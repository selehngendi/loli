"""
Free game join via matchmaking queue.
POST /join (Long Poll ~15s) → assigned → open WS immediately.
No extra sleep between retries per free-games.md.
"""
import time
from bot.api_client import MoltyAPI, APIError
from bot.utils.logger import get_logger

log = get_logger(__name__)

MAX_QUEUE_ATTEMPTS = 100       # Max attempts before giving up
MAX_QUEUE_TIME_SECONDS = 900   # 15 minutes max queuing time


async def join_free_game(api: MoltyAPI) -> tuple[str, str]:
    """
    Enter free matchmaking queue and wait for assignment.
    Returns (game_id, agent_id) when assigned.
    Raises RuntimeError if max retries or timeout exceeded.
    """
    # Idempotency guard: check queue status first
    try:
        status_resp = await api.get_join_status()
        if isinstance(status_resp, dict):
            status = status_resp.get("status", "not_queued")
            if status == "assigned":
                gid = status_resp.get("gameId", "")
                aid = status_resp.get("agentId", "")
                if gid and aid:
                    log.info("Already assigned to game: %s", gid)
                    return gid, aid
            elif status == "queued":
                log.info("Already in queue, resuming...")
    except APIError:
        pass

    # Queue loop — server Long Poll throttles (per free-games.md)
    attempt = 0
    start_time = time.monotonic()
    consecutive_errors = 0

    while attempt < MAX_QUEUE_ATTEMPTS:
        # Check total time limit
        elapsed = time.monotonic() - start_time
        if elapsed > MAX_QUEUE_TIME_SECONDS:
            raise RuntimeError(
                f"Free queue timeout after {elapsed:.0f}s ({attempt} attempts). "
                "Server may be congested — will retry next heartbeat cycle."
            )

        attempt += 1
        log.info("Free queue attempt #%d (%.0fs elapsed)...", attempt, elapsed)

        try:
            resp = await api.post_join("free")
            consecutive_errors = 0  # Reset on success

            if not isinstance(resp, dict):
                log.warning("Unexpected join response type: %s", type(resp).__name__)
                continue

            status = resp.get("status", "")

            if status == "assigned":
                gid = resp.get("gameId", "")
                aid = resp.get("agentId", "")
                if gid and aid:
                    log.info("✅ Assigned to free game: %s (agent=%s) after %d attempts",
                             gid, aid, attempt)
                    return gid, aid
                log.warning("Assigned but missing gameId/agentId: %s", resp)

            if status in ("not_selected", "queued"):
                log.debug("Queue status: %s — retrying immediately", status)
                continue

            log.warning("Unexpected queue response: %s", resp)

        except APIError as e:
            if e.code == "NO_IDENTITY":
                log.error("❌ ERC-8004 identity not registered. Cannot join free room.")
                raise
            if e.code == "OWNERSHIP_LOST":
                log.error("❌ NFT ownership changed. Re-register identity.")
                raise
            if e.code == "TOO_MANY_AGENTS_PER_IP":
                log.error("❌ IP agent limit reached for this game")
                raise
            if e.code == "ACCOUNT_ALREADY_IN_GAME":
                log.info("Already in a game. Returning to heartbeat.")
                raise
            consecutive_errors += 1
            if consecutive_errors >= 5:
                raise RuntimeError(f"Too many consecutive queue errors ({consecutive_errors}): {e}")
            log.warning("Join error: %s (consecutive=%d) — retrying", e, consecutive_errors)

    raise RuntimeError(f"Free queue exhausted after {MAX_QUEUE_ATTEMPTS} attempts")
