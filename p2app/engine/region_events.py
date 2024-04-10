from p2app.events.regions import *
import sqlite3
def searching_for_region(event, sqlconnection):
    """Function that searches for a region based on the information given in the text boxes of the Tkinter GUI.
    Returns a list of RegionSearchResultEvent, and yielded in process_event in main.py"""
    list_of_regions = []
    cur = None
    if event.name() is None and event.local_code() is None:
        cur = sqlconnection.execute('SELECT * FROM region WHERE region_code = ?;', (event.region_code(), ))
    elif event.region_code() is None and event.name() is None:
        cur = sqlconnection.execute('SELECT * FROM region WHERE local_code = ?;', (event.local_code(),))
    elif event.region_code() is None and event.local_code() is None:
        cur = sqlconnection.execute('SELECT * FROM region WHERE name = ?;', (event.name(),))
    elif event.name() is None:
        cur = sqlconnection.execute('SELECT * FROM region WHERE region_code = ? and local_code = ?;', (event.region_code(), event.local_code()))
    elif event.local_code() is None:
        cur = sqlconnection.execute('SELECT * FROM region WHERE region_code = ? and name = ?;', (event.region_code(), event.name()))
    elif event.region_code() is None:
        cur = sqlconnection.execute('SELECT * FROM region WHERE local_code = ? and name  = ?;', (event.local_code(), event.name()))
    elif event.region_code() is not None and event.name() is not None and event.region_code is not None:
        cur = sqlconnection.execute('SELECT * FROM region WHERE region_code = ? and local_code = ? and name = ?;', (event.region_code(), event.local_code(), event.name()))
    search_result = cur.fetchall()
    if search_result is not None:
        for region in search_result:
            region_search_result = RegionSearchResultEvent(Region(region[0], region[1], region[2], region[3], region[4], region[5], region[6], region[7]))
            list_of_regions.append(region_search_result)
        cur.close()
        return list_of_regions

def loading_region_event(event, sqlconnection):
    """Function that loads Edit Region window after selecting a region from the region search window.
    Returns RegionLoadedEvent and is yielded in process_event."""
    cur = sqlconnection.execute('SELECT * FROM region WHERE region_id = ?;',(event.region_id(),))
    load_result = cur.fetchone()
    if load_result is not None:
        loading_region_result = Region(load_result[0], load_result[1], load_result[2], load_result[3], load_result[4], load_result[5], load_result[6], load_result[7])
        cur.close()
        return RegionLoadedEvent(loading_region_result)

def saving_new_region_event(event,sqlconnection):
    """Function that saves a new region to the database from the New Region window.  Returns SaveRegionFailedEvent with
    an error message if any text boxes do not match the sql schema.  Returns RegionSavedEvent that is yielded in process_event."""
    try:
        if event.region_code == '' or event.region_code.isspace():
            return SaveRegionFailedEvent('Empty Region Code.')
        elif event.local_code == '' or event.local_code.isspace():
            return SaveRegionFailedEvent('Empty Local Code.')
        elif event.name == '' or event.name.isspace():
            return SaveRegionFailedEvent('Empty Name.')
        cur = sqlconnection.execute('INSERT INTO region(region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES(?,?,?,?,?,?,?);', (event.region_code, event.local_code, event.name, event.continent_id, event.country_id,event.wikipedia_link, event.keywords))
        cur = sqlconnection.execute(f'SELECT region_id FROM region WHERE region_code = \'{event.region_code}\'')
        new_id = cur.fetchone()
        new_region = Region(new_id[0], event.region_code, event.local_code, event.name, event.continent_id, event.country_id, event.wikipedia_link, event.keywords)
        sqlconnection.commit()
        cur.close()
        return RegionSavedEvent(new_region)
    except sqlite3.IntegrityError:
        return SaveRegionFailedEvent('Code is not unique.')

def editing_existing_region(event, sqlconnection):
    """Function that edits a region that is found via the Region Search window, and is updated in the database.
    Returns SaveRegionFailedEvent if any text boxes do not match the SQL schema.  Returns RegionSavedEvent and is yielded
    in process_event."""
    try:
        if event.region_code == '' or event.region_code.isspace():
            return SaveRegionFailedEvent('Empty Region Code.')
        elif event.local_code == '' or event.local_code.isspace():
            return SaveRegionFailedEvent('Empty Local Code.')
        elif event.name == '' or event.name.isspace():
            return SaveRegionFailedEvent('Empty Name.')
        cur = sqlconnection.execute(f'UPDATE region SET region_code = ? WHERE region_id = \'{event.region_id}\';', (event.region_code,))
        cur = sqlconnection.execute(f'UPDATE region SET local_code = ? WHERE region_id = \'{event.region_id}\';', (event.local_code,))
        cur = sqlconnection.execute(f'UPDATE region SET name = ? WHERE region_id = \'{event.region_id}\';', (event.name,))
        cur = sqlconnection.execute(f'UPDATE region SET continent_id = ? WHERE region_id = \'{event.region_id}\';', (event.continent_id,))
        cur = sqlconnection.execute(f'UPDATE region SET country_id = ? WHERE region_id = \'{event.region_id}\';', (event.country_id,))
        cur = sqlconnection.execute(f'UPDATE region SET wikipedia_link = ? WHERE region_id = \'{event.region_id}\';', (event.wikipedia_link,))
        cur = sqlconnection.execute(f'UPDATE region SET keywords = ? WHERE region_id = \'{event.region_id}\';', (event.keywords,))
        new_region = Region(event.region_id, event.region_code, event.local_code, event.name, event.continent_id, event.country_id, event.wikipedia_link, event.keywords)
        sqlconnection.commit()
        cur.close()
        return RegionSavedEvent(new_region)
    except sqlite3.IntegrityError:
        return SaveRegionFailedEvent('Code is not unique.')