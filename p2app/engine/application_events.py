import sqlite3

from p2app.events.database import DatabaseOpenedEvent, DatabaseClosedEvent, DatabaseOpenFailedEvent
from p2app.events.app import EndApplicationEvent
import sqlite3

def opening_database(path):
    """Opens file and checks if it is a database or not.  If not, returns DatabaseOpenFailedEvent and yielded
    in process_events in main.py.  If yes, checks if the tables continent, region, and country exist.
    If not returns DatabaseOpenFailedEvent and yielded in process_events in main.py.  If yes,
    returns DatabaseOpenedEvent and is yielded in process_events"""
    try:
        connection = sqlite3.connect(path)
        continent = 'continent'
        region = 'region'
        country = 'country'
        cur = connection.execute(f'SELECT tbl_name FROM sqlite_master WHERE name = \'{continent}\'')
        continent_check = cur.fetchone()
        if continent_check is None:
            return DatabaseOpenFailedEvent('Database invalid: missing continent table.')
        cur = connection.execute(f'SELECT tbl_name FROM sqlite_master WHERE name = \'{region}\'')
        region_check = cur.fetchone()
        if region_check is None:
            return DatabaseOpenFailedEvent('Database invalid: missing region table.')
        cur = connection.execute(f'SELECT tbl_name FROM sqlite_master WHERE name = \'{country}\'')
        country_check = cur.fetchone()
        if country_check is None:
            return DatabaseOpenFailedEvent('Database invalid: missing country table.')
        return DatabaseOpenedEvent(path)
    except sqlite3.DatabaseError:
        return DatabaseOpenFailedEvent('File is not a valid Database.')


def closing_database():
    """Closes database in the tkinter.  Returns DatabaseClosedEvent and is yielded in process_events"""
    return DatabaseClosedEvent()

def exiting_gui():
    """Ends the GUI application, returns EndApplicationEvent and is yielded in process_events"""
    return EndApplicationEvent()