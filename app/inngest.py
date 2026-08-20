import inngest

from app.state import reports

inngest_client = inngest.Inngest(
    app_id="report-api",
    is_production=False,
)


@inngest_client.create_function(
    fn_id="say-hello",
    trigger=inngest.TriggerEvent(
        event="test/hello",
    ),
)
async def say_hello(ctx: inngest.Context):
    await ctx.step.sleep(
        "wait",
        5,
    )
    return "Hello from the background!"


@inngest_client.create_function(
    fn_id="make-report",
    trigger=inngest.TriggerEvent(
        event="report/requested",
    ),
    retries=2,
)
async def make_report(ctx: inngest.Context):
    report_id = ctx.event.data["id"]
    topic = ctx.event.data["topic"]

    await ctx.step.sleep("do-the-slow-work", 8)

    async def build_report():
        if topic == "fail":
            raise Exception("The report oven is broken!")
        result = f"Report about '{topic}' is ready."
        report = reports.get(report_id)
        if report:
            report["status"] = "done"
            report["result"] = result
        return result

    return await ctx.step.run("build-report", build_report)
