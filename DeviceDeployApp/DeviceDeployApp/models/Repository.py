import sqlite3
from DeviceDeployApp.models.Search import Search
from DeviceDeployApp.models.ServerSearch import ServerSearch
from DeviceDeployApp.models.ReportSearch import ReportSearch
from werkzeug.security import generate_password_hash, check_password_hash
from DeviceDeployApp.models.Users import Users
from DeviceDeployApp.models.SignUp import SignUp

class Repository(object):

    def __init__(self):
        self.__conn = sqlite3.connect(r'Naming_Convention.sqlite')

    def __del__(self):
        self.__conn.close()
#------------------ Signing up Functions ----------------------------------
    def add_User(self, sObj):
        try:              
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute("insert into UserTable (firstName,lastName,email,pwHash) values(?,?,?,?)", (sObj.first,sObj.last,sObj.email,sObj.password))
        except Exception as e:
            # Do something here
            flash(e)
            raise  

    def check_password(self,sObj,hashPass):
        return check_password_hash(hashPass,sObj.password)

    def get_User(self,email):
        cursor = self.__conn.cursor()
        results = cursor.execute('select email from UserTable where email = "%s"' % email)
        q = results.fetchone()[0]
        return q

    def get_Permission(self, email):
        cursor = self.__conn.cursor()
        results = cursor.execute('select isAdmin from UserTable where email = "%s"' % email)
        q = results.fetchone()[0]
        return q

    def get_pwHash(self, email):
        cursor = self.__conn.cursor()
        results = cursor.execute('select pwHash from UserTable where email = "%s"' % email)
        q = results.fetchone()[0]
        return q
#-------------------------------- Device Reports Functions ----------------------------

    def get_aLoc(self, rObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Abbreviation from Device_Sites where Location = "%s"' % rObj.aLoc)
        q = results.fetchone()
        r = ["%s" % x for x in q]
        return r

    def get_aType(self, rObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Abbreviation from Device_Models where Type = "%s" group by Abbreviation' % rObj.aType)
        q = results.fetchone()
        r = ["%s" % x for x in q]
        return r

    def get_aModel(self, rObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Model from Device_Models where Model = "%s"' % rObj.aModel)
        q = results.fetchone()
        r = ["%s" % x for x in q]
        return r

    def get_Report(self, Loc, Abbr, Mod):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Location, Type, Model, Asset_Tag from Devices where Location = "%s" and Type = "%s" and Model= "%s"' % (Loc[0], Abbr[0], Mod[0]))
        q = results.fetchall()
        return q

    def make_Report(self, q):
        Loc, Type, Mod, Tag = zip(*q)
        return Loc, Type, Mod, Tag

    #-------------------Server reports----------------------
    def get_sReport(self,mode,type,module,location):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Mode, Type, Module, Location, Loc_Number from Servers where Mode = "%s" and Type = "%s" and Module= "%s" and Location = "%s"' % (mode[0], type[0], module[0],location[0]))
        q = results.fetchall()
        return q

    def get_svMode(self,rObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select code from Mode where Name = "%s"' % rObj.sMode)
        q = results.fetchall()        
        r = ["%s" % x for x in q]
        return r

    def get_svType(self, rObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Code from Type where Name = "%s"' % rObj.sType)
        q = results.fetchall()        
        r = ["%s" % x for x in q]
        return r

    def get_svModule(self, rObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Code from Module where Name = "%s"' % rObj.sMod)
        q = results.fetchall()       
        r = ["%s" % x for x in q]
        return r

    def get_svLocation(self,rObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Code from Server_Sites where Location = "%s"' % rObj.sLoc)
        q = results.fetchall()
        r = ["%s" % x for x in q]
        return r

    def make_sReport(self, q):
        Mode, Type, Module, Location, sNum = zip(*q)
        return Mode, Type, Module, Location, sNum



#------------------ Lookup Server Device Functions ----------------------------------
    def get_sLocation(self):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Location from Server_Sites')
        q = results.fetchall()
        r = ["%s" % x for x in q]
        return r

    def get_sMode(self):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Name from Mode')
        q = results.fetchall()        
        r = ["%s" % x for x in q]
        return r

    def get_sModel(self):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Name from Type')
        q = results.fetchall()        
        r = ["%s" % x for x in q]
        return r

    def get_sModule(self):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Name from Module')
        q = results.fetchall()       
        r = ["%s" % x for x in q]
        return r

    def get_servNum(self, ssObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Loc_Number from Servers where Loc_Number = "%s"' % ssObj.sNum)
        q = results.fetchone()        
        r = ["%s" % x for x in q]
        return r

    def get_Code(self, ssObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Code from Server_Sites where Location = "%s"' % ssObj.sLoc)
        q = results.fetchone()        
        r = ["%s" % x for x in q]
        return r

    def get_mCode(self, ssObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Code from Mode where Name = "%s"' % ssObj.sMode)
        q = results.fetchone()        
        r = ["%s" % x for x in q]
        return r

    def get_modCode(self, ssObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select CODE from Module where Name = "%s"' % ssObj.sModule)
        q = results.fetchone()        
        r = ["%s" % x for x in q]
        return r

    def get_tCode(self, ssObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Code from Type where Name = "%s"' % ssObj.sModel)
        q = results.fetchone()       
        r = ["%s" % x for x in q]
        return r

    def fetch_Server(self, mCode, model, module, Code, num):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Mode, Type, Module, Location, Loc_Number from Servers where Mode = "%s" and Type = "%s" and Module = "%s" and Location = "%s" and Loc_Number = "%s"' % (mCode[0], model[0], module[0], Code[0], num[0]))
        q = results.fetchall()
        return q

    #def fetch_Server(self, mCode, model, module, Code):
    #    cursor = self.__conn.cursor()
    #    results = cursor.execute('select Mode, Type, Module, Location from Servers where Mode = "%s" and Type = "%s" and Module = "%s" and Location = "%s"' % (mCode[0], model[0], module[0], Code[0]))
    #    q = results.fetchall()
    #    return q

    def make_sTable(self, q):
        mode, model, module, loc, num = zip(*q)
        return mode, model, module, loc, num

#------------------ Personal Device Functions ----------------------------------

    def get_Locations(self):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Location from Device_Sites')
        q = results.fetchall()        
        return [x[0] for x in q]

    def get_Types(self):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Abbreviation from Device_Models group by Abbreviation')
        q = results.fetchall()        
        return [x[0] for x in q]

    def get_Models(self):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Model from Device_Models group by Model')
        q = results.fetchall()        
        return [x[0] for x in q]
    
    def get_assTags(self, sObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Asset_Tag from Devices where Asset_Tag = "%s"' % sObj.assTag)
        q = results.fetchone()        
        r = ["%s" % x for x in q]
        return r

    #def get_assTags(self):
    #    cursor = self.__conn.cursor()
    #    results = cursor.execute('select Asset_Tag from Devices')
    #    q = results.fetchone()        
    #    return [x[0] for x in q]

    #Takes location from drop down menu and finds its abbreviated version
    def get_Abbreviations(self, sObj):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Abbreviation from Device_Sites where Location = "%s"' % sObj.location)
        q = results.fetchall()        
        r = ["%s" % x for x in q]
        return r

    #Fetches all filtered personal device information.
    def fetch_Device(self, sObj, Abbr, tag):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Location, Type, Model, Asset_Tag from Devices where Type = "%s" and Location = "%s" and Asset_Tag = "%s"' % (sObj.type, Abbr[0], tag[0]))
        q = results.fetchall()
        return q

    #Fetches all filtered personal device information.
    #def fetch_Device(self, sObj, Abbr):
    #    cursor = self.__conn.cursor()
    #    results = cursor.execute('select Location, Type, Model, Asset_Tag from Devices where Type = "%s" and Location = "%s"' % (sObj.type, Abbr[0]))
    #    q = results.fetchall()
    #    return q

    def check_Device(self, sObj,Abbr):
        cursor = self.__conn.cursor()
        results = cursor.execute('select Location, Type, Model, Asset_Tag from Devices where Location = "%s" and Type = "%s" and Model = "%s" and Asset_Tag = "%s"' % (Abbr[0],sObj.type,sObj.model,sObj.assTag))
        q = results.fetchall()
        return q

    def make_Table(self, q):
        Loc, Type, Mod, Tag = zip(*q)
        return Loc, Type, Mod, Tag

