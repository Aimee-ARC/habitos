# Habit Tracker App
This is a Habit Tracker desktop application built using Python and Tkinter. The app helps users create and manage daily habits, track their progress over time, and visualize statistics and trends. It also includes customizable categories and a motivational quote feature fetched from an external API.

## Features
Add and Manage Habits:
- Create new habits and assign them to specific categories.
- Modify habit names and categories.
- Delete habits when no longer needed.

Habit Completion:
- Mark habits as completed for the current day.
- View a summary of all habits and how many days they have been completed.

Categories:
- Add, modify, and delete habit categories.
- Pre-defined categories include "Salud", "Trabajo", "Ocio", "Personal", and "Estudio", which can be customized.

Statistics & Trends:
- View habit completion statistics, displaying the total number of days completed for each habit.
- Visualize trends over time for each habit using graphs.

Motivational Quotes:
- Fetch motivational quotes from the API Ninjas API and display them in the app.

## File Structure
- habit_tracker.py: Main application file with all the logic for managing habits, categories, and statistics.
- habits.json: JSON file where the habits data is stored (auto-generated).
- categories.json: JSON file where the categories data is stored (auto-generated).
- fondo.png: Background image used for the app.

## API Configuration
The app uses the API Ninjas service to fetch motivational quotes. You can modify the API key in the habit_tracker.py file:
api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
response = requests.get(api_url, headers={'X-Api-Key': 'your-api-key-here'})
