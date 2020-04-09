from requests import get
from job import * 
from re import match

class ReedAPI():
    """Class to deal with searching and set up
    Usage::
        >>> api = ReedAPI(your_api_key)
        >>> jobs = api.search(keywords='blah blah')
        >>> print(jobs[0].jobId)
        40162354
        >>> print(jobs[0].getJobsDetails().jobDescription)
        (long description with HTML)
    """
    def __init__(self, apikey, apiurl='https://www.reed.co.uk/api/1.0'):
        self.apikey = apikey
        self.apiurl = apiurl
    
    def search(self, employerId=None, employerProfileId=None, keywords=None, locationName=None, distanceFromLocation=None, permanent=None, contract=None, 
               temp=None, partTime=None, fullTime=None, minimumSalary=None, maximumSalary=None, postedByRecruitmentAgency=None, postedByDirectEmployer=None, 
               graduate=None, resultsToTake=50, resultsToSkip=0, pages=None):
        """
        Parameters mostly line up with those on the Reed API documentation. Leaving them to the default (None) will mean they're ignored.
        In the case of pages (the one arg used internally only), this represents the pages to get

        Due to the design of the API, if we haven't been told how many pages to get, we have to get one result first to figure out how 
        many requests we need to do
        Parameters:
            :param employerId=None: id of employer posting job
            :param employerProfileId=None: Profile id of employer posting job
            :param keywords=None: Search keywords. Spaces allowed (_generateURL will sanitize them)
            :param locationName=None: the location of the job 
            :param distanceFromLocation=10: distance from location name in miles (default is 10)
            :param permanent=None: true/false
            :param contract=None: true/false
            :param temp=None: true/false
            :param partTime=None: true/false
            :param fullTime=None: true/false
            :param minimumSalary=None: lowest possible salary e.g. 20000
            :param maximumSalary=None: highest possible salary e.g. 30000
            :param postedByRecruitmentAgency=None: true/false
            :param postedByDirectEmployer=None: true/false
            :param graduate=None: true/false
            :param resultsToTake=50: Page size max 100
            :param resultsToSkip=0: How many results to skip. If set to zero will be ignored. 
                Must be divisible by resultsToTake if not zero
            :param pages=None: Number of pages to get, defaults to None (all)
        Returns
            :rtype: A list of :class:`SearchJob <SearchJob>` objects (see job.py)
        Throws:
            :throw ValueError,ConnectionError:
        """
        kwargs = locals()
        if pages == 0 or type(pages) == str:
            raise ValueError('The value of pages must be an int above zero or None (the default, to get all pages)')
        self._validate(kwargs)
        jobs = []

        # Deals with needing to get all the results - the Reed API won't tell you how many results there are until 
        # a query is made
        if pages == None:
            kwargsCopy = kwargs.copy()
            kwargsCopy['resultsToTake'] = 1
            intailRequestURL = self._generateURL(kwargsCopy, self.apiurl + '/search?')
            response = get(intailRequestURL, auth=(self.apikey, ''))
            if response.status_code != 200:
                raise ConnectionError('The Reed API refused the connection. The status returned was ' + str(response.status_code))
            pages = str(response.json()['totalResults'] / resultsToTake + 1).split('.')[0]
            # response.json() doesn't work very well in this case - it errors out
            if "'totalResults': '0'" in response.text or "'totalResults': 0" in response.text or '"totalResults": 0' in response.text:
                raise ValueError('The Reed API returned zero search results')
        
        # Validate resultsToSkip value if one was set
        if kwargs['resultsToSkip'] != 0:
            if resultsToSkip % resultsToTake == 0:
                startingPage = resultsToSkip / resultsToTake
            else:
                raise ValueError('The value of resultsToSkip can not be divided by resultsToTake, so we can not calculate the starting page')
        else:
            startingPage = 1
        
        # Generate the search URL
        searchURL = self._generateURL(kwargs, self.apiurl + '/search?')
        
        # Interate for the number of times requested 
        for i in range(startingPage, int(pages)):
            # Increment resultsToSkip so we don't keep getting the same page
            kwargs['resultsToSkip'] = kwargs['resultsToSkip'] + resultsToTake

            searchURL = self._generateURL(kwargs, self.apiurl + '/search?')
            response = get(searchURL, auth=(self.apikey, ''))

            if response.status_code == 200:
                for job in response.json()['results']:
                    jobs.append(SearchJob(job, self.apikey, self.apiurl))
            else:
                raise ConnectionError('The Reed API refused the connection. The status returned was ' + str(response.status_code))
        return jobs

    def _generateURL(self, kwargs, URLBase):
        """
        Turn a dict into a URL 
            :param kwargs: Dict of keyword arguments
            :param URLBase: The base URL
            :rtype: str
        """  
        count = 0
        for arg in kwargs:
            if arg == 'pages' or kwargs[arg] == 0 or kwargs[arg] == None:
                continue
            else:
                value = str(kwargs[arg]).replace(' ', '%20').replace('True', 'true').replace('False', 'false').replace('None', 'null')
                if count == 0:
                    URLBase += arg + '=' + value
                else:
                    URLBase += '&' + arg + '=' + value
                count += 1
        return URLBase

    def _validate(self, kwargs):
        """
        Validate that the parameters that are limited to true/false actually have the correct value
            :param kwargs: Dict of arguments to check
            :throw ValueError: if the value is wrong 
            :rtype: True
        """
        for arg in kwargs:
            if match('^(permanent|contract|temp|partTime|fullTime|postedByRecruitmentAgency|postedByDirectEmployer|graduate)$', arg):
                if not match('^(true|false|True|False|None)$', str(kwargs[arg])):
                    raise ValueError('The argument ' + arg + ' needs to be a boolean value or None (the default). It\'s actually ' + str(kwargs[arg]))
        return True