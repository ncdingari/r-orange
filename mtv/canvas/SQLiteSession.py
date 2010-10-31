## SQLiteSession.  Implimentation of sqlite functions for Red-R.  
import redREnviron, sqlite3, os, time, cPickle

class SQLiteHandler:
    def __init__(self, defaultDB = None):
        if defaultDB:
            self.dataBase = defaultDB
        else:
            self.dataBase = 'local|temp.db'
            
    def getDatabase(self, dataBase = None):
        if not dataBase:
            dataBase = self.dataBase
        if 'local|' in dataBase:  # convert the database if the local name is present.
            database = os.path.join(redREnviron.directoryNames['tempDir'], dataBase.split('|')[1])
        else:
            database = dataBase
        return database
        
    def execute(self, query, parameters = None, database = None):
        conn = sqlite3.connect(self.getDatabase(database))
        cursor = conn.cursor()
        response = []
        try:
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            for row in cursor:
                response.append(row)
        except Exception as inst:
            import log
            log.logException(inst)
            #pass
        finally:
            #import log
            #log.logException(query)
            conn.commit()
            conn.close()
            return response
    def getColumnNames(self, table, database = None):
        if not database:
            database = self.dataBase
        response = self.execute('PRAGMA table_info('+table+')', database = database)
        
        colnames = []
        for row in response:
            colnames.append(str(row[1]))
            
        return colnames
        
    def setTable(self, table, colNames, database = None, force = False):
        if not database:
            database = self.dataBase
        if force:
            self.execute('DROP TABLE IF EXISTS '+table, database = database)
        try:
            self.execute("CREATE TABLE "+table+" "+colNames, database = database)
        except Exception as inst:
            print inst
    def getTableNames(self, database = None):
        
        response = self.execute('SELECT * FROM SQLITE_MASTER WHERE type="table" OR type ="view"', database = database)
        info = []
        for row in response:  # collect the info for all of the tables and the views.
            info.append(str(row[1])+', '+ str(row[0]))
            print row
        return info
        
    def newTableName(self):
        return 'AutoTable_'+str(time.time()).replace('.', '_')
    def newIDName(self):
        return 'AutoID_'+str(time.time()).replace('.', '_')
    def dictToTable(self, dictionary, tableName = None, database = None):
        if not database:
            database = self.dataBase
        if not tableName:
            tableName = self.newTableName()
        self.setTable(tableName, '("Name" text, "Data" text)', database = database, force = True)
        for name in dictionary.keys():
            self.execute("insert into "+tableName+" values (?,?)", parameters = (cPickle.dumps(name), cPickle.dumps(dictionary[name])), database = database)
        return tableName
        
    def tableToDict(self, tableName, dataBase = None):
        if not dataBase:
            dataBase = self.dataBase
        response = self.execute('select * from '+tableName, database = dataBase)
        newDict = {}
        for row in response:
            newDict[cPickle.loads(str(row[0]))] = cPickle.loads(str(row[1]))
            
        return newDict
        
    def saveObject(self, object):
        tableName = 'SavedObjects'
        dataBase = 'local|SavedObjects.db'
        self.setTable(tableName, '("ID" key, "Data" text)', database = dataBase)
        newID = self.newIDName()
        self.execute('insert into SavedObjects values (?,?)', parameters = (newID, cPickle.dumps(object)), database = dataBase)
        return newID
        
    def setObject(self, oldID):
        #print oldID
        tableName = 'SavedObjects'
        dataBase = 'local|SavedObjects.db'
        response = self.execute('select * from SavedObjects where ID = ?', parameters = (oldID,), database = dataBase)
        self.execute('DELETE FROM '+tableName+' WHERE ID = ?', parameters = (oldID, ), database = dataBase) ## delete the ref
        #print str(response) 
        return cPickle.loads(str(response[0][1]))