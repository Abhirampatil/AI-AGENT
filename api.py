import os
import httpx
import requests
# import pytz
# from datetime import datetime
from livekit.agents import llm
from typing import Annotated

# DATE AND TIME BLOCK
# def get_current_datetime():
#     current_datetime = datetime.now()
#     formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     return formatted_datetime

#     if __name__ == "__main__":
#         current_datetime = get_current_datetime()
#         print("Current Date and Time:", current_time)




# WEATHER BLOCK
@llm.ai_callable()
async def get_weather(
    location: Annotated[str, llm.TypeInfo(description="The location to get the weather for")]
):
    """
    Retrieves weather information for the specified location using the OpenWeatherMap API.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "OpenWeatherMap API key is not set. Please add OPENWEATHER_API_KEY to your .env file."

    # Build the request URL (using metric units for temperature)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        return f"Error fetching weather data: {response.text}"

    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]

    # The timezone func is not working
    # timezone = pytz.timezone('Asia/Kolkata')
    # current_datetime = datetime.now()
    # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


    return f"The weather in {location} is {description} with a temperature of {temp}°C."






# NEWS BLOCK

def get_trending_news(api_key, country='in', category=None):

    # "https://newsapi.org/v2/everything"         FOR ALL TYPES OF NEWS
    # "https://newsapi.org/v2/top-headlines"      FOR TOP HEADLINES

    url = "https://newsapi.org/v2/top-headlines?sources=google-news-in"
    params = {
        'apiKey': api_key,
        'country': country,
    }
    if category:
        params['category'] = category

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [article['title'] for article in data.get('articles', [])]
    else:
        print(f"Error: Unable to fetch news (Status Code: {response.status_code})")
        return []

# Example usage
if __name__ == "__main__":
    # Replace 'your_api_key_here' with your actual NewsAPI key
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("NewsAPI API key is not set. Please add NEWSAPI_API_KEY to your .env file.")
        exit(1)
    trending_news = get_trending_news(api_key)
    # trending_news = get_trending_news(api_key, country='in', category='technology')
    print("Trending News:")
    for idx, news in enumerate(trending_news, start=1):
        print(f"{idx}. {news}")



