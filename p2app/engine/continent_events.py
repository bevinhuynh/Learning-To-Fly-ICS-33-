from p2app.events.continents import *
import sqlite3

def searching_for_continent(event, sqlconnection):
    """Function that searches for a continent based on the information given in the text boxes of the Tkinter GUI.
            Returns a list of ContinentSearchResultEvent, and yielded in process_event in main.py"""
    list_of_continents = []
    cur = None
    if event.name() is None:
        cur = sqlconnection.execute('SELECT * FROM continent WHERE continent_code = ?;',(event.continent_code(),))
    elif event.continent_code() is None:
        cur = sqlconnection.execute('SELECT * FROM continent WHERE name = ?;', (event.name(),))
    elif event.continent_code() is not None and event.name() is not None:
        cur = sqlconnection.execute('SELECT * FROM continent WHERE continent_code = ? and name = ?;', (event.continent_code(), event.name()))
    search_result = cur.fetchall()
    if search_result is not None:
        for continent in search_result:
            continent_search_result = ContinentSearchResultEvent(Continent(continent[0], continent[1], continent[2]))
            list_of_continents.append(continent_search_result)
        cur.close()
        return list_of_continents



def loading_continent_event(event, sqlconnection):
    """Function that loads Edit Continent window after selecting a continent from the continent search window.
           Returns ContinentLoadedEvent and is yielded in process_event."""
    cur = sqlconnection.execute('SELECT * FROM continent WHERE continent_id = ?;',(event.continent_id(),))
    load_result = cur.fetchone()
    if load_result is not None:
        loading_continent_result = Continent(load_result[0], load_result[1], load_result[2])
        cur.close()
        return ContinentLoadedEvent(loading_continent_result)


def saving_new_continent_event(event, sqlconnection):
    """Function that saves a new continent to the database from the New Continent window.  Returns SaveContinentFailedEvent with
         an error message if info in text boxes do not match the SQL Schema.  Returns ContinentSavedEvent and is yielded in process_event"""
    try:
        if (event.name == '' or event.name.isspace()) and (event.continent_code == "" or event.continent_code.isspace()):
            return SaveContinentFailedEvent('Both columns were left empty.')
        elif event.name.isspace() or event.name == '':
            return SaveContinentFailedEvent('Empty Name.')
        elif event.continent_code.isspace() or event.continent_code == '':
            return SaveContinentFailedEvent('Empty Code.')
        cur = sqlconnection.execute('INSERT INTO continent(continent_code, name) VALUES(?,?);', (event.continent_code, event.name))
        cur = sqlconnection.execute(f'SELECT continent_id FROM continent WHERE continent_code = \'{event.continent_code}\' ')
        new_id = cur.fetchone()
        new_continent = Continent(new_id[0], event.continent_code, event.name)
        sqlconnection.commit()
        cur.close()
        return ContinentSavedEvent(new_continent)
    except sqlite3.IntegrityError:
        return SaveContinentFailedEvent('Code is not Unique.')
def editing_saved_continent(event, sqlconnection):
    """Function that edits a continent that is found via the Continent Search window, and is updated in the database.
            Returns SaveContinentFailedEvent if any text boxes do not match the SQL schema.  Returns ContinentSavedEvent and is yielded
            in process_event."""
    try:
        if (event.name == '' or event.name.isspace()) and (event.continent_code == "" or event.continent_code.isspace()):
            return SaveContinentFailedEvent('Both columns were left empty.')
        elif event.name.isspace() or event.name == '':
            return SaveContinentFailedEvent('Empty Name.')
        elif event.continent_code.isspace() or event.continent_code == '':
            return SaveContinentFailedEvent('Empty Code.')
        cur = sqlconnection.execute(f'UPDATE continent SET continent_code = ? WHERE continent_id = \'{event.continent_id}\';', (event.continent_code,))
        cur = sqlconnection.execute(f'UPDATE continent SET name = ? WHERE continent_id = \'{event.continent_id}\';', (event.name,))
        updated_continent = Continent(event.continent_id, event.continent_code, event.name)
        sqlconnection.commit()
        cur.close()
        return ContinentSavedEvent(updated_continent)
    except sqlite3.IntegrityError:
        return SaveContinentFailedEvent('Code is not Unique.')


