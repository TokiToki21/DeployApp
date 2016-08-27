"""
Routes and views for the flask application.
"""
# imports
from flask import Flask, url_for, request, render_template, abort, redirect, flash, session
from functools import wraps
from DeviceDeployApp import app
from DeviceDeployApp.models.Search import Search
from DeviceDeployApp.models.ServerSearch import ServerSearch
from DeviceDeployApp.models.ReportSearch import ReportSearch, ServerReportSearch
from DeviceDeployApp.models.Repository import Repository
from DeviceDeployApp.models.Users import Users
from DeviceDeployApp.models.SignUp import SignUp

# holder for repository 
repo = Repository()

@app.route('/', methods=['GET', 'POST'])
def home():
    """Renders the home page"""
    if request.method == 'GET':
        return render_template('index.html', title='Welcome')

@app.route('/sUp', methods=['GET','POST'])
def signUp():

    # Renders the Sign Up page
    if request.method == 'GET':
        return render_template('SignUp.html',title='Sign Up')  
    elif request.method == 'POST':
        # retrieve form data
        fName= request.form['firstName']
        lName = request.form['lastName']
        email = request.form['email']        
        password = request.form['password']
        # implement form data to User Table
        sObj = SignUp(fName,lName,email,password)
        repo.add_User(sObj)
        return render_template('SignSuccess.html', title='Success')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():
    """
    use this for login testing
        admin: raam@raam.com        password: Testing1
        user: tyler@tyler.com      password: Testing2 
    """
    # redirecting checks
    next = request.args.get("next")
    
    # Renders the login page
    if request.method == 'GET':
        return render_template('Login.html', next = next)

    #elif request.method == 'POST': 
    email = request.form['email']
    passwd = request.form['password']
    user = repo.get_User(email)
    getPerm = repo.get_Permission(email)
    getPWHASH = repo.get_pwHash(email)
    perm = 0
    
    # if user is admin give admin rights else give standard rights
    if user:
        if getPerm is 1:
            perm = 1
        else:
            perm = 0
    # create user object
    sObj = Users(email,passwd,perm)

    if user and repo.check_password(sObj, getPWHASH):
        session['email'] = email
        if next:
            return redirect(next)
        else:
            return redirect(url_for('home'))
    else:
        flash("Username or password was incorrect")
        return redirect(url_for('login'))    

# decorator for login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else:
            flash("A login is required to see the page!")
            return redirect(url_for('login', next=request.path))
    return decorated_function
# decorator for permissions
def requires_permissions(permissions):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if repo.get_Permission(session['email']) is permissions:
                return f(*args, **kwargs)
            else:
                abort(403)
        return wrapped
    return wrapper

@app.route('/lookup', methods=['GET','POST'])
@login_required
@requires_permissions(1)
def lookup():
    """Renders the lookup page."""
    if request.method == 'GET':
        locations = repo.get_Locations()
        types = repo.get_Types()
        models = repo.get_Models()
        return render_template('Lookup.html', title="Lookups", 
                               loca = locations, types = types, models = models)

    elif request.method == 'POST':
        location = request.form['ltLOC']
        type = request.form['ltType']
        model = request.form['ltModel']
        assTag = request.form['assTag']
        sObj = Search(location,type,model,assTag)

        #Pulls Database data 
        dbData = repo.fetch_Device(sObj, repo.get_Abbreviations(sObj), repo.get_assTags(sObj))

        #Breaks lists of tuples from data into 4 seperate lists
        l, t, m, a = repo.make_Table(dbData)
        
        #Saves different lists in 1 variable
        table_rows = zip(l, t, m, a)

        return render_template('LookupResults.html', Table_data = table_rows)
    return 


@app.route('/servlookup', methods=['GET','POST'])
@login_required
@requires_permissions(1)
def servlookup():
    """Renders the reports page."""
    if request.method == 'GET':
        sLoc = repo.get_sLocation()
        sMode = repo.get_sMode()
        sModel = repo.get_sModel() 
        sModule = repo.get_sModule() 
                      
        return render_template('ServerLookup.html', title="Server Lookup", sLoca = sLoc, sMode = sMode, sModel = sModel, sModule = sModule)

    elif request.method == 'POST':
        sMode = request.form['servMode']
        sModel = request.form['servModel']
        sModule = request.form['servModule']
        sLoc = request.form['servLoc']
        sNum = request.form['servNum']

        ssObj = ServerSearch(sMode, sModel, sModule, sLoc, sNum)

        #Pulls Database data 
        servDB = repo.fetch_Server(repo.get_mCode(ssObj), repo.get_tCode(ssObj), repo.get_modCode(ssObj), repo.get_Code(ssObj),repo.get_servNum(ssObj))

        #Breaks lists of tuples from data into 4 seperate lists
        s1, s2, s3, s4, s5 = repo.make_sTable(servDB)
        
        #Saves different lists in 1 variable
        sTable_rows = zip(s1, s2, s3, s4, s5)

        return render_template('ServerTable.html', sTable_data = sTable_rows)
    return

@app.route('/reports', methods=['GET'])
@login_required
def reports():
    """Renders the reports page."""
    if request.method == 'GET':
        return render_template('Reports.html',title='Reports')

@app.route('/dReports', methods=['GET','POST'])
@login_required
def dReports():
    """Renders the reports page."""
    if request.method == 'GET':
        return render_template('DeviceReport.html',title='Device Reports')

    elif request.method == 'POST':
        aLoc = request.form['aLoc']
        aType = request.form['aType']
        aModel = request.form['aModel']
   
        rObj = ReportSearch(aLoc, aType, aModel)
        
        report = repo.get_Report(repo.get_aLoc(rObj), repo.get_aType(rObj), repo.get_aModel(rObj))

        Loc, Type, Mod, Tag = repo.make_Report(report)
        ReportRows = zip(Loc, Type, Mod, Tag)

        return render_template('ReportResults.html', rRows = ReportRows)

@app.route('/sReports', methods=['GET','POST'])
@login_required
def sReports():
    """Renders the reports page."""
    if request.method == 'GET':
        return render_template('ServerReport.html',title='Server Reports')

    elif request.method == 'POST':
        sMode = request.form['sMode']
        sType = request.form['sType']
        sMod = request.form['sMod']
        sLoc = request.form['sLoc']        
   
        rObj = ServerReportSearch(sMode, sType, sMod, sLoc)
        
        report = repo.get_sReport(repo.get_svMode(rObj), repo.get_svType(rObj), repo.get_svModule(rObj), repo.get_svLocation(rObj))

        Mode, Type, Module, Location, sNum = repo.make_sReport(report)
        ReportRows = zip(Mode, Type, Module, Location, sNum)

        return render_template('ReportResults.html', sRows = ReportRows)

@app.route('/lookupresult', methods=['GET','POST'])
@login_required
def lookupresult():
    """Renders the reports page."""
    if request.method == 'GET':
        return render_template('LookupResults.html',title='Lookup Results')

