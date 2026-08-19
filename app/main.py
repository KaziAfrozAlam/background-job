from fastapi import FastAPI, status
import inngest

from inngest.fast_api import serve

from app.inngest import (
    generate_report,
    inngest_client,
    say_hello,
)


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reports", status_code=status.HTTP_202_ACCEPTED)
async def create_report():
    await inngest_client.send(
        inngest.Event(
            name="report/generate",
        )
    )

    return {"status": "accepted"}


serve(
    app,
    inngest_client,
    [say_hello, generate_report],
)