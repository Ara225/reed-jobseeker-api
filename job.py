from datetime import datetime
from webbrowser import open_new_tab
from requests import get

class Job():
    """Job base class"""
    def __init__(self, Jobdict, apikey, apiurl):
        self.apikey = apikey
        self.apiurl = apiurl
        for item in Jobdict:
            if "date" in item.lower():
                # convert dates to datetime objects
                setattr(self, item, datetime.strptime(Jobdict[item], '%d/%m/%Y'))
            else:
                setattr(self, item, Jobdict[item])
    
    def openReedURL(self):
        """Open Reed URL in new tab in default browser. Returns a bool """
        return open_new_tab(self.jobUrl)

    def openExternalURL(self):
        """Open external URL in new tab in default browser Returns a bool"""
        if self.externalUrl == None:
            return False
        else:
            return open_new_tab(self.jobUrl)
    
class SearchJob(Job):
    """For the jobs in search results. Need an easy way to get the details of the job"""
    def getJobsDetails(self):
        response = get(self.apiurl + '/jobs/' + str(self.jobId), auth=(self.apikey, ''))
        return Job(response.json(), self.apikey, self.apiurl)