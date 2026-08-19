from fastapi import FastAPI
from inngest.fast_api import serve

from app.inngest import inngest_client, say_hello


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


serve(
    app,
    inngest_client,
    [say_hello],
)