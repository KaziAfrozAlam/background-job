import inngest


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
    fn_id="generate-report",
    trigger=inngest.TriggerEvent(
        event="report/generate",
    ),
)
async def generate_report(ctx: inngest.Context):
    await ctx.step.sleep(
        "generate",
        8,
    )

    return "Report generated"
