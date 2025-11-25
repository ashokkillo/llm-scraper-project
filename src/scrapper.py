import json, argparse, os, time
from tqdm import tqdm
from jira_client import JiraClient
from state import StateStore
from transform import transform_issue_to_jsonl

def main(projects):
    client = JiraClient()
    state = StateStore()

    os.makedirs("output", exist_ok=True)

    for project in projects:
        print(f"\n📌 Scraping project: {project}")
        startAt = state.get(project, 0)

        jql = f"project = {project} ORDER BY created ASC"
        pbar = tqdm(desc=f"{project}", unit="issue")

        while True:
            data = client.search(jql, startAt=startAt, maxResults=100)
            issues = data.get("issues", [])
            if not issues:
                break

            for issue in issues:
                obj = transform_issue_to_jsonl(issue, client)
                with open(f"output/{project.lower()}.jsonl", "a", encoding="utf8") as f:
                    f.write(json.dumps(obj, ensure_ascii=False) + "\n")

                startAt += 1
                state.update(project, startAt)
                pbar.update(1)

            if startAt >= data.get("total", 0):
                break

            time.sleep(0.2)  # polite throttle

        pbar.close()
        print(f"✔ Done: {project}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--projects", nargs="+", required=True)
    args = parser.parse_args()
    main(args.projects)
