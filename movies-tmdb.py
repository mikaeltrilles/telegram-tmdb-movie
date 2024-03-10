import argparse
import requests
import subprocess
import os
import sys
from datetime import datetime

# Correspondance entre les ID de genre et les emojis
genre_mapping = {
    28: '💪 #Action',
    16: '🐵 #Animation',
    12: '🌋 #Aventure',
    35: '😂 #Comédie',
    80: '🔪 #Crime',
    18: '🎭 #Drame',
    99: '🌍 #Documentaire',
    10762: '👶🏻 #Enfant',
    10751: '👨‍👩‍👦‍👦 #Familial',
    14: '🦄 #Fantastique',
    10752: '💣 #Guerre',
    36: '👑 #Histoire',
    27: '😱 #Horreur',
    10402: '🎸 #Musique',
    9648: '🧙🏻‍♂️ #Mystère',
    10749: '💕 #Romance',
    878: '🤖 #SciFi',
    10770: '📺 #Telefilm',
    53: '🚓 #Thriller',
    37: '🌵 #Western',
    10764: '🎱 #Reality',
    10765: '🚀 #Science-Fiction_&_Fantastique',
    10759: '👊🏻 #Action_&_Adventure',
}

# Correspondance entre les noms de pays et les emojis
country_mapping = {
    'South Africa': '🇿🇦 #Afrique_du_Sud',
    'Germany': '🇩🇪 #Allemagne',
    'Algeria': '🇩🇿 #Algérie',
    'Saudi Arabia': '🇸🇦 #Arabie_Saoudite',
    'Argentina': '🇦🇷 #Argentine',
    'Australia': '🇦🇺 #Australie',
    'Austria': '🇦🇹 #Autriche',
    'Belgium': '🇧🇪 #Belgique',
    'Brazil': '🇧🇷 #Brésil',
    'Canada': '🇨🇦 #Canada',
    'Chile': '🇨🇱 #Chili',
    'China': '🇨🇳 #Chine',
    'Colombia': '🇨🇴 #Colombie',
    'South Korea': '🇰🇷 #Corée_du_sud',
    'Denmark': '🇩🇰 #Danemark',
    'Spain': '🇪🇸 #Espagne',
    'United States of America': '🇺🇸 #États_Unis',
    'Finland': '🇫🇮 #Finlande',
    'France': '🇫🇷 #France',
    'Hong Kong': '🇭🇰 #Hong_Kong',
    'Hungary': '🇭🇺 #Hongrie',
    'India': '🇮🇳 #Inde',
    'Italy': '🇮🇹 #Italie',
    'Iran': '🇮🇷 #Iran',
    'Ireland': '🇮🇪 #Irlande',
    'Iceland': '🇮🇸 #Islande',
    'Japan': '🇯🇵 #Japon',
    'Kenya': '🇰🇪 #Kenya',
    'Luxembourg': '🇱🇺 #Luxembourg',
    'Malta': '🇲🇹 #Malte',
    'Morocco': '🇲🇦 #Maroc',
    'Mexico': '🇲🇽 #Mexique',
    'New Zealand': '🇳🇿 #Nouvelle_Zelande',
    'Norway': '🇳🇴 #Norvège',
    'Pakistan': '🇵🇰 #Pakistan',
    'Netherlands': '🇳🇱 #Pays_Bas',
    'Poland': '🇵🇱 #Pologne',
    'Portugal': '🇵🇹 #Portugal',
    'Dominican Republic': '🇩🇴 #République_Dominicaine',
    'United Kingdom': '🇬🇧 #Royaume_Uni',
    'Russia': '🇷🇺 #Russie',
    'Senegal': '🇸🇳 #Sénégal',
    'Sweden': '🇸🇪 #Suède',
    'Switzerland': '🇨🇭 #Suisse',
    'Czech Republic': '🇨🇿 #Tchéquie',
    'Turkey': '🇹🇷 #Turquie',
    'Ukraine': '🇺🇦 #Ukraine',
    'Estonia': '🇪🇪 #Estonie',

}


def get_movie_details(api_key, movie_id):
    base_url = f'https://api.themoviedb.org/3/movie/{
        movie_id}?api_key={api_key}&language=fr-FR'
    response = requests.get(base_url)
    return response.json()


def get_cast_details(api_key, movie_id):
    credits_url = f'https://api.themoviedb.org/3/movie/{
        movie_id}/credits?api_key={api_key}&language=fr-FR'
    response = requests.get(credits_url)
    return response.json() if response.status_code == 200 else None


def minutes_to_hours(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours:02d}h{remaining_minutes:02d}"


def generate_html(movie_details, cast_details):
    try:
        html_content = ""

        genres_with_emojis = [genre_mapping.get(
            genre['id'], '') for genre in movie_details['genres']]
        genres_html = ' • '.join(genres_with_emojis)

        # # Vérifier si une tagline existe
        # tagline = f"<i>{movie_details['tagline']}</>" if 'tagline' in movie_details and movie_details['tagline'] else '...'

        # Vérifier si la balise tagline existe et n'est pas vide
        if 'tagline' in movie_details and movie_details['tagline']:
            tagline_html = f"\n<i>{movie_details['tagline']}</>\n"
        else:
            tagline_html = ' '

        # Formater la date de sortie en format européen
        release_date = datetime.strptime(
            movie_details['release_date'], '%Y-%m-%d').strftime('%d/%m/%Y')

        # Convertir les pays en emojis
        countries_emoji = [country_mapping.get(
            country['name'], '') for country in movie_details.get('production_countries', [])]
        countries_html = ' • '.join(countries_emoji)

        # Ajouter les liens TMDB et IMDB
        tmdb_link = f"<a href='https://www.themoviedb.org/movie/{
            movie_details['id']}'>🎬 TMDB</>"
        imdb_link = f"<dot> <a href='https://www.imdb.com/title/{
            movie_details['imdb_id']}'>⭐️ IMDB</>"

        # Vérifier si le titre original existe, sinon utiliser le titre en français
        title = movie_details['title']
        original_title = movie_details.get('original_title', '')
        release_year = datetime.strptime(
            movie_details['release_date'], '%Y-%m-%d').strftime('%Y')
        title_html = f"<b>{title} ({release_year})</>"
        if original_title and original_title != title:
            title_html += f"<br><b>Titre Original:</> {original_title}"

        # Arrondir vote_average à deux chiffres après la virgule s'il y a une note, sinon "NC" (Non Classé)
        vote_average_rounded = round(movie_details.get(
            'vote_average', 'NC'), 2) if 'vote_average' in movie_details else 'nc'

        # Convertir la durée en format "hh:mm"
        runtime_formatted = minutes_to_hours(movie_details['runtime'])

        # Extraire tous les noms des membres de l'équipe de réalisation ayant le job "Director"
        directors = [member['name'] for member in cast_details['crew'] if member['job'] == 'Director']

        # Si des réalisateurs sont disponibles, les utiliser, sinon "NC"
        director_html = ', '.join(directors) if directors else 'nc'

        # Vérifier si les détails du casting sont disponibles
        if 'cast' in cast_details:
            # Obtenez la liste des membres de la distribution
            cast_members = cast_details['cast']

            # Si la liste des membres de la distribution est disponible, l'utiliser, sinon "NC"
            if cast_members:
                # Limiter aux 10 premiers acteurs
                cast_html = ', '.join(
                    [f"{member['name']}" for member in cast_members[:10]])
            else:
                cast_html = 'nc'
        else:
            cast_html = 'nc'

        html_content = f"""{title_html}
<b>Origines:</> {countries_html}
<b>Date de Sortie:</> {release_date}
<b>Durée:</> {runtime_formatted}min ⭐️ <b>{vote_average_rounded}</>/10
<b>Réalisateur:</b> {director_html}
<b>Acteurs :</b> {cast_html}
<b>Genres:</> {genres_html}
{tagline_html}
<b>Synopsis:</>
<m>{movie_details['overview']}</>

{tmdb_link} {imdb_link}

<b>Affiche:</><img src="https://image.tmdb.org/t/p/w500/{movie_details['poster_path']}">
"""

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return html_content


def generate_markdown(movie_details, cast_details):
    try:
        markdown_content = ""

        genres_with_emojis = [genre_mapping.get(
            genre['id'], '') for genre in movie_details['genres']]
        genres_markdown = ' • '.join(genres_with_emojis)

        # Vérifier si la balise tagline existe et n'est pas vide
        if 'tagline' in movie_details and movie_details['tagline']:
            tagline_markdown = f"\n__{movie_details['tagline']}__\n"
        else:
            tagline_markdown = ' '

        # Formater la date de sortie en format européen
        release_date = datetime.strptime(
            movie_details['release_date'], '%Y-%m-%d').strftime('%d/%m/%Y')

        # Convertir les pays en emojis
        countries_emoji = [country_mapping.get(
            country['name'], '') for country in movie_details.get('production_countries', [])]
        countries_markdown = ' • '.join(countries_emoji)

        # Ajouter les liens TMDB et IMDB
        tmdb_link = f"[🎬 TMDB](https://www.themoviedb.org/movie/{movie_details['id']})"
        imdb_link = f"[⭐️ IMDB](https://www.imdb.com/title/{movie_details['imdb_id']})"

        # Vérifier si le titre original existe, sinon utiliser le titre en français
        title = movie_details['title']
        original_title = movie_details.get('original_title', '')
        release_year = datetime.strptime(
            movie_details['release_date'], '%Y-%m-%d').strftime('%Y')
        title_markdown = f"**{title} ({release_year})**"
        if original_title and original_title != title:
            title_markdown += f"\n**Titre Original:** {original_title}"

        # Arrondir vote_average à deux chiffres après la virgule s'il y a une note, sinon "NC" (Non Classé)
        vote_average_rounded = round(movie_details.get(
            'vote_average', 'NC'), 2) if 'vote_average' in movie_details else 'nc'

        # Convertir la durée en format "hh:mm"
        runtime_formatted = minutes_to_hours(movie_details['runtime'])

        # Extraire tous les noms des membres de l'équipe de réalisation ayant le job "Director"
        directors = [member['name']
                     for member in cast_details['crew'] if member['job'] == 'Director']

        # Si des réalisateurs sont disponibles, les utiliser, sinon "NC"
        director_markdown = ', '.join(directors) if directors else 'nc'

        # Vérifier si les détails du casting sont disponibles
        if 'cast' in cast_details:
            # Obtenez la liste des membres de la distribution
            cast_members = cast_details['cast']

            # Si la liste des membres de la distribution est disponible, l'utiliser, sinon "NC"
            if cast_members:
                # Limiter aux 10 premiers acteurs
                cast_markdown = ', '.join(
                    [f"{member['name']}" for member in cast_members[:10]])
            else:
                cast_markdown = 'nc'
        else:
            cast_markdown = 'nc'

        markdown_content = f"""{title_markdown}
**Origines:** {countries_markdown}
**Date de Sortie:** {release_date}
**Durée:** {runtime_formatted}min ⭐️ **{vote_average_rounded}**/10
**Réalisateur:** {director_markdown}
**Acteurs :** {cast_markdown}
**Genres:** {genres_markdown}
{tagline_markdown}
**Synopsis:**
{movie_details['overview']}

{tmdb_link} {imdb_link}

**Affiche:** ![Affiche](https://image.tmdb.org/t/p/w500/{movie_details['poster_path']})
"""

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return markdown_content


if __name__ == "__main__":
    # Remplacez 'VOTRE_CLE_API' par votre clé API réelle
    api_key = '09a87b0b9f15b8b28f3a6927593ad6b0'

    # Configurer les arguments en ligne de commande
    parser = argparse.ArgumentParser(
        description="Générer une fiche de présentation de film à partir de l'API TMDb.")
    parser.add_argument("movie_id", type=str, help="L'ID du film sur TMDb")

    # Analyser les arguments
    args = parser.parse_args()

    # Obtenir les détails du film
    movie_details = get_movie_details(api_key, args.movie_id)

    # Obtenir les détails du casting
    cast_details = get_cast_details(api_key, args.movie_id)

if cast_details is not None:
    # Génère la fiche HTML
    html_content = generate_html(movie_details, cast_details)

    # Ajouter les liens TMDB et IMDB à la fiche HTML
    tmdb_link = f"<a href='https://www.themoviedb.org/movie/{
        movie_details['id']}'>🎬 TMDB</>"
    imdb_link = f" • <a href='https://www.imdb.com/title/{
        movie_details['imdb_id']}'>⭐️ IMDB</>"

    # Génère la fiche Markdown
    markdown_content = generate_markdown(movie_details, cast_details)

    # Ajoute le contenu Markdown à la fiche HTML
    html_content += f"\n\n---\n\n{markdown_content}"

    # Enregistre la fiche HTML dans un fichier
    html_file_path = f"tmkprojectlist/movies/{args.movie_id}.html"
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    # # Vérifie si le fichier HTML existe
    if os.path.exists(html_file_path):
        # Ouvre le fichier HTML dans Visual Studio Code avec la prévisualisation
        subprocess.run(
            ["code", "--file-uri", f"file://{os.path.abspath(html_file_path)}"])


    else:
        print(f"Le fichier HTML {html_file_path} n'existe pas.")
else:
    print(f"Les détails du casting ne sont pas disponibles.")
