#!/usr/bin/env python3

import os
import json
import requests
import sys

PROMPT_CAFE_ENDPOINT = "https://prompt-cafe-production.up.railway.app/api/generate"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
SEND_BODY_TO_SLACK = os.environ.get("SEND_BODY_TO_SLACK", "false").lower() in ("1","true","yes")

if not SLACK_WEBHOOK_URL:
    print("ERROR: SLACK_WEBHOOK_URL not set")
    sys.exit(1)

def main():
    try:
        r = requests.post(PROMPT_CAFE_ENDPOINT, timeout=120)
    except Exception as e:
        requests.post(SLACK_WEBHOOK_URL, json={"text": f"🚨 prompt cafe call failure: {e}"})
        sys.exit(1)

    status = r.status_code

    body_preview = None
    try:
        j = r.json()
        body_preview = json.dumps(j, indent=2)[:3000]
    except:
        body_preview = (r.text or "")[:3000]

    if SEND_BODY_TO_SLACK:
        txt = f"Prompt Cafe status: {status}\n```{body_preview}```"
    else:
        txt = f"Prompt Cafe status: {status}"

    requests.post(SLACK_WEBHOOK_URL, json={"text": txt})
    print("done")

if __name__ == "__main__":
    main()
