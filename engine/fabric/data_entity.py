import sqlite3
# from fabric.configuration import Configuration
from fabric.logging import Logger   # Use with great caution - recursion trap !
from pprint import pprint, pformat

# log = Logger()
# cfg = Configuration()

class DataEntity():
    '''
    Data entity (table) handler for SQLite
    '''
    database = None
    table = None
    attributes = []
    table_exists = False

    def __init__(self, database=None, table=None, attributes=None):
        '''
        DataEntity class constructor
        Parameters:
            self: instance of the class
            table: entity table name
            attributes: entity table columns
        Returns:
            None
        '''
        log = Logger()

        if (database is not None):
            self.database = database
        else:
            self.database = 'noisebin.db'

        if (table is not None):
            self.table = table

        if (attributes is not None):
            self.attributes = attributes

        if (self.table is None):
            raise sqlite3.Warning(f'No data entity specified.  I\'m confused.')
            # doesn't continue

        log.debug(f'{self.table}.table_exists is: {self.table_exists}')
        if (self.table_exists):
            # table exists - store the attributes for reference (may not be as specified at entry)
            self.attributes = dict(result)
            cursor.close();
        else:
            # we don't remember this table existing, but let's check the database
            probe_sql = f'SELECT name, type FROM PRAGMA_TABLE_INFO("{self.table}");'
            conn = sqlite3.connect(self.database)
            cursor = conn.execute(probe_sql)
            result = cursor.fetchall()

            # log.debug(f'Schema query result: {pformat(result)}')
            if (result == []):
                # No table, but can we make one?
                # log.debug(f'{self.table} table not found in {self.database}')

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
                # schema for table found
                self.table_exists = True

            # log.debug(f'{self.table} attributes are: {pformat(self.attributes)}')

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
            # log.debug(f'event.store: Extracting values from event: {pformat(datum)}\n')
            # log.debug(f'event.store: ... with templating from: {pformat(self.attributes)}\n')

            s1 = 'INSERT INTO ' + self.table + ' ('
            s2 = ') VALUES ('
            for a in self.attributes.keys():
                s1 += f'{a}, '
                s2 += f'\'{datum[a]}\', '
            store_sql = s1[:-2] + s2[:-2] + ')'

            # log.debug(f'Store SQL: {store_sql}')

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
        log = Logger()

        # log.debug(f'query() vars: {pformat(vars(self))}')
        if (not self.table_exists):
            raise sqlite3.Warning(f'Table {self.table} does not exist when querying data.')
        else:
            # log.debug(f'{self.table} Query: {query}')

            conn = sqlite3.connect(self.database)
            cursor = conn.execute(query)
            result = cursor.fetchall()
            conn.commit()
            conn.close()

            return result
