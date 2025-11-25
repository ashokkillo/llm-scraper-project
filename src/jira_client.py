import time, random, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE = "https://issues.apache.org/jira/rest/api/2"

def make_session():
    retry = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429,500,502,503,504]
    )
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s

def handle_rate(resp):
    if resp.status_code == 429:
        wait = resp.headers.get("Retry-After")
        wait = int(wait) if wait else random.uniform(1.0, 3.0)
        time.sleep(wait)
        return True
    return False

class JiraClient:
    def __init__(self, timeout=30):
        self.s = make_session()
        self.timeout = timeout

    def search(self, jql, startAt=0, maxResults=50):
        url = f"{BASE}/search"
        params = {
            "jql": jql,
            "startAt": startAt,
            "maxResults": maxResults,
            "expand": "renderedFields"
        }
        while True:
            resp = self.s.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json()
            if handle_rate(resp):
                continue
            resp.raise_for_status()

    def get_issue(self, key):
        url = f"{BASE}/issue/{key}"
        params = {"expand": "comments,changelog,renderedFields"}
        while True:
            resp = self.s.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json()
            if handle_rate(resp):
                continue
            resp.raise_for_status()
