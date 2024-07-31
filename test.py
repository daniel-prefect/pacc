from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect.artifacts import create_markdown_artifact
import httpx

@task(retries=3, log_prints=True, cache_key_fn=task_input_hash)
def fetch_weather(lat: float = 38.9, lon: float = -77.0):
    base_url = "https://api.open-meteo.com/v1/forecast"
    temps = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    forecasted_temp = float(temps.json()["hourly"]["temperature_2m"][0])
    print(f"Forecasted temperature: {forecasted_temp} degrees")
    return forecasted_temp

@task()
def save_weather(temp: float):
    with open("weather.csv", "w") as f:
        f.write(f"{temp}")
    return "Temperature saved!"

@flow()
def pipeline(lat: float = 38.9, lon: float = -78.0):
    temp = fetch_weather(lat, lon)

    # Create a markdown artifact
    text = f"""# Weather Forecast
    {temp}
    """
    create_markdown_artifact(
        key="weather-result",
        markdown=text,
        description="Weather forecast"
    )

    result = save_weather(temp)
    return result

if __name__ == "__main__":
    pipeline.serve(name="deploy-1")