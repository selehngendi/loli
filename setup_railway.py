"""
Railway Variable Setup — Set all env vars for Molty Royale bot.
Usage: python setup_railway.py <RAILWAY_API_TOKEN>

Get your token from: https://railway.com/account/tokens
"""
import sys
import json
import urllib.request

RAILWAY_GQL = "https://backboard.railway.app/graphql/v2"

# Variables to set (bot will auto-generate API_KEY, wallets, etc on first run)
VARIABLES = {
    "AGENT_NAME": "MoltyAgent",
    "ROOM_MODE": "free",
    "LOG_LEVEL": "INFO",
    "ADVANCED_MODE": "true",
    "AUTO_WHITELIST": "true",
    "AUTO_SC_WALLET": "true",
    "ENABLE_MEMORY": "true",
    "ENABLE_AGENT_TOKEN": "false",
    "AUTO_IDENTITY": "true",
    "AGGRESSION_LEVEL": "balanced",
}


def gql(token: str, query: str, variables: dict = None) -> dict:
    """Execute GraphQL query against Railway API."""
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        RAILWAY_GQL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_projects(token: str) -> list:
    """List all Railway projects."""
    result = gql(token, """
        query { me { projects { edges { node { id name } } } } }
    """)
    edges = result.get("data", {}).get("me", {}).get("projects", {}).get("edges", [])
    return [e["node"] for e in edges]


def get_services(token: str, project_id: str) -> list:
    """List services in a project."""
    result = gql(token, """
        query($projectId: String!) {
            project(id: $projectId) {
                services { edges { node { id name } } }
            }
        }
    """, {"projectId": project_id})
    edges = result.get("data", {}).get("project", {}).get("services", {}).get("edges", [])
    return [e["node"] for e in edges]


def get_environments(token: str, project_id: str) -> list:
    """List environments in a project."""
    result = gql(token, """
        query($projectId: String!) {
            project(id: $projectId) {
                environments { edges { node { id name } } }
            }
        }
    """, {"projectId": project_id})
    edges = result.get("data", {}).get("project", {}).get("environments", {}).get("edges", [])
    return [e["node"] for e in edges]


def upsert_variables(token: str, project_id: str, environment_id: str,
                     service_id: str, variables: dict) -> dict:
    """Set multiple variables at once using variableCollectionUpsert."""
    result = gql(token, """
        mutation($input: VariableCollectionUpsertInput!) {
            variableCollectionUpsert(input: $input)
        }
    """, {
        "input": {
            "projectId": project_id,
            "environmentId": environment_id,
            "serviceId": service_id,
            "variables": variables,
        }
    })
    return result


def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("  Railway Variable Setup for Molty Royale Bot")
        print("=" * 60)
        print()
        print("Usage: python setup_railway.py <RAILWAY_API_TOKEN>")
        print()
        print("Get your token from:")
        print("  https://railway.com/account/tokens")
        print()
        print("Variables that will be set:")
        for k, v in VARIABLES.items():
            print(f"  {k} = {v}")
        print()
        print("Bot will auto-generate on first run:")
        print("  API_KEY, AGENT_PRIVATE_KEY, AGENT_WALLET_ADDRESS,")
        print("  OWNER_EOA, OWNER_PRIVATE_KEY")
        sys.exit(1)

    token = sys.argv[1]

    # Also add RAILWAY_API_TOKEN to variables so bot can auto-sync
    all_vars = {**VARIABLES, "RAILWAY_API_TOKEN": token}

    print("🔍 Fetching projects...")
    projects = get_projects(token)
    if not projects:
        print("❌ No projects found. Create a project on Railway first.")
        sys.exit(1)

    # Find project containing "lola" service or let user pick
    target_project = None
    target_service = None
    for proj in projects:
        services = get_services(token, proj["id"])
        for svc in services:
            if "lola" in svc["name"].lower():
                target_project = proj
                target_service = svc
                break
        if target_service:
            break

    if not target_project:
        print("Available projects:")
        for i, p in enumerate(projects):
            print(f"  [{i}] {p['name']} (id={p['id'][:12]}...)")
        idx = int(input("Select project number: "))
        target_project = projects[idx]
        services = get_services(token, target_project["id"])
        if services:
            print("Available services:")
            for i, s in enumerate(services):
                print(f"  [{i}] {s['name']}")
            sidx = int(input("Select service number: "))
            target_service = services[sidx]

    if not target_service:
        print("❌ No service found. Deploy a service on Railway first.")
        sys.exit(1)

    print(f"✅ Project: {target_project['name']}")
    print(f"✅ Service: {target_service['name']}")

    # Get environment
    envs = get_environments(token, target_project["id"])
    if not envs:
        print("❌ No environments found.")
        sys.exit(1)

    # Use first environment (usually "production")
    env = envs[0]
    print(f"✅ Environment: {env['name']}")

    # Set variables
    print(f"\n📦 Setting {len(all_vars)} variables...")
    result = upsert_variables(
        token, target_project["id"], env["id"],
        target_service["id"], all_vars,
    )

    if "errors" in result:
        print(f"❌ Error: {result['errors']}")
        sys.exit(1)

    print("✅ Variables set successfully!")
    print()
    for k, v in all_vars.items():
        display_v = v[:8] + "..." if k in ("RAILWAY_API_TOKEN",) else v
        print(f"  {k} = {display_v}")
    print()
    print("🚀 Bot will auto-generate credentials on first deploy!")


if __name__ == "__main__":
    main()
