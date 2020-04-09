import unittest
from main import ReedAPI
from sys import argv
from job import *

class Test(unittest.TestCase):
    def test_instigate_api(self):
        api = ReedAPI(apikey)
    
    def test_generate_url(self):
        """Make sure the URL generating function is working"""
        api = ReedAPI(apikey)
        generatedURL = api._generateURL({'keywords': 'software development', 'graduate': True, 'locationName': 'London'}, 'https://www.reed.co.uk/api/1.0/search?')
        self.assertEqual(generatedURL, api.apiurl + '/search?keywords=software%20development&graduate=true&locationName=London')

    def test_search_jobs(self):
        """Test basic job searching, as the result will vary, simply confirms it's an instance of SearchJob"""
        api = ReedAPI(apikey)
        result = api.search(keywords='software development', locationName='London', graduate=True)
        self.assertIsInstance(result[0], SearchJob)
    
    def test_search_jobs_with_paging(self):
        """Same as above but using paging"""
        api = ReedAPI(apikey)
        result = api.search(keywords='software development', graduate=True, pages=2)
        self.assertIsInstance(result[0], SearchJob)
        # Hopfully the total results are always more than 200 :)
        self.assertEqual(len(result), 200)
        # Make sure pages aren't repeated 
        self.assertNotEqual(result[0].jobId, result[101].jobId)

    def test_call_validate_with_invalid_parameters(self):
        """Ensure correct handling of this error condition (contract must have a true/false value)"""
        api = ReedAPI(apikey)
        with self.assertRaises(ValueError):
            api._validate({'keywords':'software development', 'contract': 563926})
    
    def test_search_jobs_with_zero_pages(self):
        """Ensure correct handling of this error condition (pages must not be zero)"""
        api = ReedAPI(apikey)
        with self.assertRaises(ValueError):
            api.search({'keywords':'software development', 'locationName': 'London', 'pages': 0})

    def test_search_jobs_and_get_job_details(self):
        """ Get jobs details, and confirm object type"""
        api = ReedAPI(apikey)
        result = api.search(keywords='software development', locationName='London', pages=1)
        self.assertIsInstance(result[0].getJobsDetails(), Job)

if __name__ == '__main__':
    # unittest will take the arg as a testcase selector so we need to pop it out of the list before it sees it
    apikey = argv[1]
    argv.pop(1)
    unittest.main()