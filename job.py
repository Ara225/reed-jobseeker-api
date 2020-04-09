from datetime import datetime
from webbrowser import open_new_tab
from requests import get

class Job():
    def __init__(self, Jobdict, apikey, apiurl):
        self.apikey = apikey
        self.apiurl = apiurl
        for item in Jobdict:
            if "date" in item.lower():
                setattr(self, item, datetime.strptime(Jobdict[item], '%d/%m/%Y'))
            else:
                setattr(self, item, Jobdict[item])
    
    def openReedURL(self):
        return open_new_tab(self.jobUrl)

    def openExternalURL(self):
        if self.externalUrl == None:
            return False
        else:
            return open_new_tab(self.jobUrl)

    
class SearchJob(Job):
    def getJobsDetails(self):
        response = get(self.apiurl + '/jobs/' + str(self.jobId), auth=(self.apikey, ''))
        return Job(response.json(), self.apikey, self.apiurl)


        

