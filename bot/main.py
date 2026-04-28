"""
Molty Royale AI Agent Fleet — Entry Point v3.0
Runs N agents concurrently in one process.

Config via env vars:
  AGENT_COUNT=10        → number of concurrent agents (default: 1)

Per-agent credentials (i = 1..N):
  AGENT_{i}_NAME        = "MoltyAgent1"
  AGENT_{i}_API_KEY     = ""   (auto-generated on first run)
  AGENT_{i}_PRIVATE_KEY = ""   (auto-generated)
  AGENT_{i}_WALLET_ADDRESS = ""
  AGENT_{i}_OWNER_EOA   = ""
  AGENT_{i}_OWNER_KEY   = ""

Run: python -m bot.main
"""
import asyncio
import os
import sys
from bot.agent_runner import AgentRunner
from bot.dashboard.server import start_dashboard
from bot.utils.logger import get_logger

log = get_logger(__name__)

DASHBOARD_PORT = int(os.getenv("PORT", os.getenv("DASHBOARD_PORT", "8080")))
AGENT_COUNT = int(os.getenv("AGENT_COUNT", "1"))


async def run_all():
    log.info("╔══════════════════════════════════════════════╗")
    log.info("║  MOLTY ROYALE AI FLEET  v3.0                ║")
    log.info("║  Agents: %-3d                                 ║", AGENT_COUNT)
    log.info("╚══════════════════════════════════════════════╝")

    # Dashboard server (shared for all agents)
    await start_dashboard(port=DASHBOARD_PORT)

    # Spawn all agents as concurrent coroutines
    runners = [AgentRunner(i) for i in range(1, AGENT_COUNT + 1)]
    tasks = [asyncio.create_task(r.run(), name=f"agent-{r.index}")
             for r in runners]

    log.info("🚀 Launched %d agent(s) concurrently", AGENT_COUNT)

    # Wait forever — tasks run indefinitely
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        log.info("Shutdown signal received, stopping all agents...")
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


def main():
    """Entry point."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(run_all())
    except KeyboardInterrupt:
        log.info("Shutdown complete.")


if __name__ == "__main__":
    main()
