# Covid-Tracker-Bot

Project for HackED 2021
In this project we created a discord bot which used the Johns Jopkins university api to fetch covid-19 related data, this data is displayed using various commands listed below

| Commands    |                                    Description                                   |
| ----------- | -------------------------------------------------------------------------------- |
| !commands (country)  | Lists all other commands                                                |
| !cases (country)     | Displays the number of cases of selected country                        |
| !deaths (country)    | Displays the number of deaths of selected country                       |
| !recovered (country) | Displays the number of recovered people of selected country             |
| !tests (country)     | Displays the number of people tested in selected country                |
| !critical (country)  | Displays the number of people in critical condition in selected country |
| !rank (int)          | Displays the top (param) rank of countries based on number of deaths    |

### How to Run:
    python bot.py

### Dependencies:
    pip install covid
    pip install discord.py
    pip install wikipedia
