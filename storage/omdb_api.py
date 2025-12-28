import requests

API_KEY = "9e0ecada"
BASE_URL = "http://www.omdbapi.com/"

def fetch_movie_from_api(title):


    """Fetch movie data from OMDb API by title."""
    params = {"apikey": API_KEY, "t": title}

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()
    except requests.exceptions.RequestException:
        return None, "API_CONNECTION_ERROR"

    if data.get("Response") == "False":
        return None, "MOVIE_NOT_FOUND"

    return {
        "title": data["Title"],
        "year": int(data["Year"]),
        "rating": float(data["imdbRating"]),
        "poster": data["Poster"]
    }, None

