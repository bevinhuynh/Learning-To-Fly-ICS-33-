# p2app/engine/main.py
#
# ICS 33 Fall 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.


import sqlite3
from p2app.events.database import OpenDatabaseEvent, CloseDatabaseEvent
from p2app.engine.application_events import opening_database, closing_database, exiting_gui
from p2app.events.app import QuitInitiatedEvent
from p2app.events.continents import *
from p2app.engine.continent_events import searching_for_continent, loading_continent_event, saving_new_continent_event, editing_saved_continent
from p2app.events.countries import *
from p2app.engine.country_events import searching_for_country, loading_country_event, saving_new_country, editing_existing_country
from p2app.events.regions import *
from p2app.engine.region_events import searching_for_region, loading_region_event, saving_new_region_event, editing_existing_region


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the path towards the database and the SQLite 3 connection."""
        self.path = None
        self.connection = None



    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if isinstance(event, OpenDatabaseEvent):
            self.path = event.path()
            self.connection = sqlite3.connect(event.path())
            yield opening_database(event.path())

        if isinstance(event, CloseDatabaseEvent):
            yield closing_database()

        if isinstance(event, QuitInitiatedEvent):
            yield exiting_gui()

        if isinstance(event, StartContinentSearchEvent):
            yield from searching_for_continent(event, self.connection)

        if isinstance(event, LoadContinentEvent):
            yield loading_continent_event(event, self.connection)

        if isinstance(event,SaveNewContinentEvent):
            yield saving_new_continent_event(event.continent(), self.connection)

        if isinstance(event,SaveContinentEvent):
            yield editing_saved_continent(event.continent(), self.connection)

        if isinstance(event, StartCountrySearchEvent):
            yield from searching_for_country(event, self.connection)

        if isinstance(event, LoadCountryEvent):
            yield  loading_country_event(event,self.connection)

        if isinstance(event, SaveNewCountryEvent):
            yield saving_new_country(event.country(), self.connection)

        if isinstance(event, SaveCountryEvent):
            yield editing_existing_country(event.country(), self.connection)

        if isinstance(event, StartRegionSearchEvent):
            yield from searching_for_region(event, self.connection)

        if isinstance(event, LoadRegionEvent):
            yield loading_region_event(event, self.connection)

        if isinstance(event,SaveNewRegionEvent):
            yield saving_new_region_event(event.region(),self.connection)

        if isinstance(event, SaveRegionEvent):
            yield editing_existing_region(event.region(), self.connection)












