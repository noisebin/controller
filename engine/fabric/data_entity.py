import sqlite3
from fabric.configuration import Configuration
from fabric.logging import Logger
from pprint import pprint, pformat

# from fabric.logging import Logger # Use with great caution - recursion trap !
log = Logger()

cfg = Configuration()

DEFAULT_DATA_TYPE = 'TEXT'
ATTRIBUTES_LIST = ['timestamp', 'device_type', 'name', 'metric', 'value']

class DataEntity():
    '''
    Data entity (table) handler for SQLite
    '''
    table = None
    attributes = []
    table_exists = False

    def __init__(self, name=None, attributes=None):
        '''
        DataEntity class constructor
        Parameters:
            self: instance of the class
            table: entity table name
            attributes_list: entity table columns
        Returns:
            None
        '''

        settings = cfg.params
        if (('database' in settings) and (settings['database'] is not None)):
            self.database = settings['database']
        else:
            self.database = 'noisebin.db'

        if (name is not None):
            self.table = name

        if (attributes is not None):
            self.attributes = attributes

        if (self.table is None):
            raise sqlite3.Warning(f'No data entity specified.  I\'m confused.')
        else:
            if (not self.table_exists):
                # we don't remember this table existing, but let's check the database
                probe_sql = f'SELECT name, type FROM PRAGMA_TABLE_INFO("{self.table}");'
                conn = sqlite3.connect(self.database)
                cursor = conn.execute(probe_sql)
                result = cursor.fetchall()

                log.debug(f'Schema query result: {pformat(result)}')
                if (result == []):
                    # No table, but can we make one?
                    log.debug(f'{self.table} table not found in {self.database}')

                    if (len(self.attributes)):  # Yes, we can!
                        create_table_sql = 'CREATE TABLE IF NOT EXISTS ' + self.table + ' ('
                        for a in self.attributes.keys():
                            # log.debug(f'Have attribute {a} of type {self.attributes[a]}')
                            create_table_sql += f'{a} {self.attributes[a]}, '
                        create_table_sql = create_table_sql[:-2] + ')'
                        log.debug(f'Creating {self.table} with: {create_table_sql}')
                        conn.execute(create_table_sql)
                        conn.commit()  # boo-whacka-boom-bam!
                        conn.close()
                        self.table_exists = True
                    else:
                        self.table_exists = False
                        raise sqlite3.Warning(f'Table {self.table} does not exist and we don\'t have enough wood to make one')

                else:
                    # table exists - store the attributes for reference (may not be as specified at entry)
                    self.attributes = dict(result)
                    self.table_exists = True
                    cursor.close();

            log.debug(f'Table {self.table} {"exists" if self.table_exists else "does not exist"}')
            log.debug(f'{self.table} attributes are: {pformat(self.attributes)}')

    def store(self, datum):
        '''
        Store the event
        Parameters:
            self: active instance object of this class
            datum: dict of datum/row/tuple to be stored
        Returns:
            None
        '''

        if (not self.table_exists):
            raise sqlite3.Warning(f'Table {self.table} does not exist when storing data.')
        else:
            # log.debug(f'event.store: Extracting values from event: {vars(event)}\n')
            print(f'event.store: Extracting values from event: {pformat(datum)}\n')
            print(f'event.store: Templating from: {pformat(self.attributes)}\n')

            s1 = 'INSERT INTO ' + self.table + ' ('
            s2 = ') VALUES ('
            for a in self.attributes.keys():
                s1 += f'{a}, '
                s2 += f'\'{datum[a]}\', '
            store_sql = s1[:-2] + s2[:-2] + ')'

            # insert_sql = f'INSERT INTO event (timestamp, device_type, name, pin, state) \
                # VALUES ("{event.timestamp}", "{event.device_type}", "{event.name}", "{event.pin}", {event.state});'

            log.debug(f'Store SQL: {store_sql}')

            conn = sqlite3.connect(self.database)
            conn.execute(store_sql)
            conn.commit()
            conn.close()

    def query(self, query):
        '''
        Generic query on the table
        Parameters:
            self: active instance object of this class
            query: complete & final SQL statement
        Returns:
            None
        '''

        if (not self.table_exists):
            raise sqlite3.Warning(f'Table {self.table} does not exist when querying data.')
        else:
            log.debug(f'{self.table} Query: {query}')

            conn = sqlite3.connect(self.database)
            cursor = conn.execute(query)
            result = cursor.fetchall()
            conn.commit()
            conn.close()

            return result
