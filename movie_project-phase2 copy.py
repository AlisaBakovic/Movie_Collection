import random
import movie_storage_sql as storage
from movie_collection.omdb_api import fetch_movie_from_api


def program_exit():


    """Exits the program and prints a goodbye message."""
    print("Bye!")


def list_movies():


    """Retrieve and display all movies from the database."""
    movies = storage.get_movies()
    print(f"{len(movies)} movies in total")

    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")



def add_movie():


    """Add a new movie to the database."""
    title = input("Enter movie title: ")

    movie_data, error = fetch_movie_from_api(title)

    if error == "MOVIE_NOT_FOUND":
        print("Movie not found in OMDb.")
        return

    if error == "API_CONNECTION_ERROR":
        print("Cannot connect to OMDb API.")
        return

    storage.add_movie(movie_data["title"],
                      movie_data["year"],
                      movie_data["rating"],
                      movie_data["poster"]
                      )

def generate_website():


    movies = storage.get_movies()

    movie_grid = '<ol class="movie-grid">\n'
    for title, data in movies.items():
        movie_grid += f"""  <li class="movie">
            <img class="movie-poster" src="{data['poster']}" alt="{title} poster">
            <div class="movie-title">{title}</div>
            <div class="movie-year">{data['year']}</div>
            <div class="movie-rating">Rating: {data['rating']}</div>
        </li>\n"""
    movie_grid += '</ol>'


    with open("_static/index_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html_content = template.replace("__TEMPLATE_TITLE__", "My Movie Collection")
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    with open("_static/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Website was generated successfully.")

def delete_movie():


    """Delete a movie from the database."""
    title = input("Enter movie title to delete: ")
    storage.delete_movie(title)


def update_movie():


    """Update a movie rating in the database."""
    title = input("Enter movie title to update: ")
    try:
        rating = float(input("Enter new rating: "))
    except ValueError:
        print("Rating must be a number!")
        return
    storage.update_movie(title, rating)

def stats():


    """Displays average, median, best, and worst movie ratings."""
    movies = storage.get_movies()
    average_rating = sum(movie["rating"] for movie in movies) / len(movies)
    best_movie = max(movies, key=lambda movie: movie["rating"])
    worst_movie = min(movies, key=lambda movie: movie["rating"])

    movies_rating = sorted([movie["rating"] for movie in movies])

    if len(movies_rating) % 2 == 0:
        left = len(movies_rating) // 2 - 1
        right = len(movies_rating) // 2
        median_value = (movies_rating[left] + movies_rating[right]) / 2

    else:
        mid = len(movies_rating) // 2
        median_value = movies_rating[mid]

    print(f"Average rating: {average_rating:.2f} ")
    print(f"Best movie: {best_movie["title"]}, {best_movie["rating"]}")
    print(f"Worst movie: {worst_movie["title"]}, {worst_movie["rating"]}")
    print(f"Median rating: {median_value:.2f}")

    return


def random_movie():


    """Selects and displays a random movie from the list."""
    movies = storage.get_movies()
    random_movie = random.choice(movies)

    title = random_movie["title"]
    rating = random_movie["rating"]
    year = random_movie["year"]

    print(f"Today you should watch '{title}' ({year}) - {rating} ")

    return


def search_movie():


    """Searches for a movie by partial name and prints the first match."""
    movies = storage.get_movies()
    while True:
        search_input = str(input("Enter part of movie name: ")).strip().lower()
        found = False

        for movie in movies:
            if search_input in movie["title"].lower():
                print(f"Found: {movie["title"]} ({movie["year"]}) - {movie["rating"]}")
                found = True
                break

        if not found:
            print("Nothing found.")
            continue

        break


def movie_by_rating():


    """Sorts and prints all movies by rating in ascending order."""
    movies = storage.get_movies()
    sorted_movies_by_rating = sorted(movies, key=lambda movie: movie["rating"])

    print(f"Sorted movies by rating:")
    for index, movie in enumerate(sorted_movies_by_rating, start=1):
        print(f"{index}. {movie["title"]} ({movie["year"]}) - {movie["rating"]}")

    return


def movie_by_year():


    """Sorts and prints all movies by release year in ascending order."""
    movies = storage.get_movies()
    sorted_movies_by_year = sorted(movies, key=lambda movie: movie["year"])
    for index, movie in enumerate(sorted_movies_by_year, start=1):
        print(f"{index}. {movie["title"]} ({movie["year"]}) - {movie["rating"]}")
    return


def filter_movie():


    """Filters movies based on user-specified rating and year range."""
    movies = storage.get_movies()

    input_min_rating = float(input("Enter minimum rating: "))
    input_start_year = int(input("Enter start year: "))
    input_end_year = int(input("Enter end year: "))

    for movie in movies:
        if (input_min_rating <= movie["rating"] and
                input_start_year <= movie["year"] <= input_end_year):
            print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    return


def main():


    """Displays menu, takes user choice, and runs selected function."""
    menu_tasks = {
        "exit": program_exit,
        "list_movies": list_movies,
        "add_movie": add_movie,
        "delete_movie": delete_movie,
        "update_movie": update_movie,
        "stats": stats,
        "random_movie": random_movie,
        "search_movie": search_movie,
        "movie_by_rating": movie_by_rating,
        "movie_by_year": movie_by_year,
        "filter_movie": filter_movie,
        "generate_website": generate_website

    }

    menu_list = list(menu_tasks.items())

    for index, (key, value) in enumerate(menu_list, start=0):
        print(f"{index}. {key.replace("_", " ").title()}")

    while True:
        try:
            user_input = int(input("Enter choice (0-10): "))

            if 0 <= user_input < len(menu_list):
                selected_function = menu_list[user_input][1]

                if selected_function == program_exit:
                    selected_function()
                    break
                else:
                    selected_function()
        except ValueError:
            pass


if __name__ == "__main__":
    main()
