from prefect import flow
import os

@flow(log_prints=True)
def my_flow(name: str = "World"):
    print(f"Hello, {os.environ['MY_ENV_VAR']}!")

if __name__ == "__main__":
    my_flow.from_source(
        source="https://github.com/daniel-prefect/pacc.git",
        entrypoint="deploy.py:my_flow",
    ).deploy(
        name="pacc_deployment",
        work_pool_name="test",
    )