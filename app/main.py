import uuid

import inngest
from fastapi import FastAPI, HTTPException, status
from inngest.fast_api import serve
from pydantic import BaseModel

from app.inngest import inngest_client, make_report, say_hello
from app.state import reports

app = FastAPI()


class ReportRequest(BaseModel):
    topic: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reports", status_code=status.HTTP_202_ACCEPTED)
async def create_report(body: ReportRequest):
    if not body.topic:
        raise HTTPException(status_code=400, detail="topic is required")

    report_id = str(uuid.uuid4())
    reports[report_id] = {
        "id": report_id,
        "topic": body.topic,
        "status": "pending",
    }

    await inngest_client.send(
        inngest.Event(
            name="report/requested",
            data={"id": report_id, "topic": body.topic},
        )
    )

    return {"id": report_id, "status": "pending"}


@app.get("/reports/{report_id}")
def get_report(report_id: str):
    report = reports.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="report not found")
    return report


serve(
    app,
    inngest_client,
    [say_hello, make_report],
)
