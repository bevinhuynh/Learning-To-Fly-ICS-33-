import tkinter

from p2app.events.countries import Country, CountrySavedEvent, SaveCountryFailedEvent, CountrySearchResultEvent, CountryLoadedEvent
import sqlite3

def searching_for_country(event, sqlconnection):
    """Function that searches for a country based on the information given in the text boxes of the Tkinter GUI.
        Returns a list of CountrySearchResultEvent, and yielded in process_event in main.py"""
    list_of_countries = []
    cur = None
    if event.name() is None:
        cur = sqlconnection.execute('SELECT * FROM country WHERE country_code = ?;',(event.country_code(),))
    elif event.country_code() is None:
        cur = sqlconnection.execute('SELECT * FROM country WHERE name = ?;', (event.name(),))
    elif event.country_code() is not None and event.name() is not None:
        cur = sqlconnection.execute('SELECT * FROM country WHERE country_code = ? and name = ?;',(event.country_code(), event.name()))
    search_result = cur.fetchall()
    if search_result is not None:
        for country in search_result:
            country_search_result = CountrySearchResultEvent(Country(country[0], country[1], country[2], country[3], country[4], country[5]))
            list_of_countries.append(country_search_result)
        cur.close()
        return list_of_countries

def loading_country_event(event, sqlconnection):
    """Function that loads Edit Country window after selecting a country from the country search window.
       Returns CountryLoadedEvent and is yielded in process_event."""
    cur = sqlconnection.execute('SELECT * FROM country WHERE country_id = ?;',(event.country_id(),))
    load_result = cur.fetchone()
    if load_result is not None:
        loading_continent_result = Country(load_result[0], load_result[1], load_result[2], load_result[3], load_result[4], load_result[5])
        cur.close()
        return CountryLoadedEvent(loading_continent_result)

def saving_new_country(event,sqlconnection):
     """Function that saves a new country to the database from the New Country window.  Returns SaveCountryFailedEvent with
     an error message if info in text boxes do not match the SQL Schema.  Returns CountrySavedEvent and is yielded in process_event"""
     try:
         if event.name.isspace() or event.name == '':
            return SaveCountryFailedEvent('Empty Name.')
         elif event.country_code.isspace() or event.country_code == '':
            return SaveCountryFailedEvent('Empty Code.')
         elif event.wikipedia_link is None:
            return SaveCountryFailedEvent('Empty wikipedia link.')
         elif event.wikipedia_link.isspace():
             return SaveCountryFailedEvent('Empty wikipedia link.')
         cur = sqlconnection.execute('INSERT INTO country(country_code, name, continent_id, wikipedia_link, keywords) VALUES(?,?,?,?,?);', (event.country_code, event.name, event.continent_id, event.wikipedia_link, event.keywords))
         cur = sqlconnection.execute(f'SELECT country_id FROM country WHERE country_code = \'{event.country_code}\' ')
         new_id = cur.fetchone()
         new_country = Country(new_id[0], event.country_code,event.name,event.continent_id,event.wikipedia_link,event.keywords)
         sqlconnection.commit()
         cur.close()
         return CountrySavedEvent(new_country)
     except sqlite3.IntegrityError:
        return SaveCountryFailedEvent('Code is not unique.')


def editing_existing_country(event, sqlconnection):
    """Function that edits a country that is found via the Country Search window, and is updated in the database.
    Returns SaveCountryFailedEvent if any text boxes do not match the SQL schema.  Returns CountrySavedEvent and is yielded
    in process_event."""
    try:
        if event.name.isspace() or event.name == '':
            return SaveCountryFailedEvent('Empty Name.')
        elif event.country_code.isspace() or event.country_code == '':
            return SaveCountryFailedEvent('Empty Code.')
        elif event.wikipedia_link is None:
            return SaveCountryFailedEvent('Empty wikipedia link.')
        elif event.wikipedia_link.isspace():
            return SaveCountryFailedEvent('Empty wikipedia link.')
        cur = sqlconnection.execute(f'UPDATE country SET country_code = ? WHERE country_id = \'{event.country_id}\';', (event.country_code,))
        cur = sqlconnection.execute(f'UPDATE country SET name = ? WHERE country_id = \'{event.country_id}\';', (event.name,))
        cur = sqlconnection.execute(f'UPDATE country SET continent_id = ? WHERE country_id = \'{event.country_id}\';', (event.continent_id,))
        cur = sqlconnection.execute(f'UPDATE country SET wikipedia_link = ? WHERE country_id = \'{event.country_id}\';', (event.wikipedia_link,))
        cur = sqlconnection.execute(f'UPDATE country SET keywords = ? WHERE country_id = \'{event.country_id}\';', (event.keywords,))
        updated_country = Country(event.country_id, event.country_code, event.name, event.continent_id,event.wikipedia_link,event.keywords)
        sqlconnection.commit()
        cur.close()
        return CountrySavedEvent(updated_country)
    except sqlite3.IntegrityError:
        return SaveCountryFailedEvent('Code is not unique.')




