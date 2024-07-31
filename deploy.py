from prefect import flow

@flow(log_prints=True)
def my_flow(name: str = "World"):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    my_flow.from_source(
        source="...",
        entrypoint="deploy.py:my_flow",
    ).deploy(
        name="pacc_deployment",
        work_pool_name="test",
    )