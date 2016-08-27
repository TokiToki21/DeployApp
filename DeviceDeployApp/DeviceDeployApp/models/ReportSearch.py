class ReportSearch(object):
    def __init__(self,aLoc,aType,aModel):
        self.aLoc = aLoc.title()
        self.aType = aType.title()
        self.aModel = aModel
       
class ServerReportSearch(object):
    def __init__(self, sMode, sType, sMod, sLoc):
        self.sMode = sMode.title()
        self.sType = sType.title()
        self.sMod = sMod.title()
        self.sLoc = sLoc.title()      