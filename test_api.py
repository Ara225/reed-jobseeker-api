import unittest
from main import ReedAPI
from sys import argv

class Test(unittest.TestCase):
    def test_instigate_api(self):
        api = ReedAPI(apikey)
    
    def test_generate_url(self):
        api = ReedAPI(apikey)
        generatedURL = api._generateURL({'keywords': 'software development', 'graduate': True}, 'https://www.reed.co.uk/api/1.0/search?')
        self.assertEqual(generatedURL, api.apiurl + '/search?keywords=software%20development&graduate=true')

    def test_search_jobs(self):
        api = ReedAPI(apikey)
        api.search(keywords='software development')

    def test_search_jobs_and_get_job_details(self):
        pass

if __name__ == '__main__':
    apikey = argv[1]
    argv.pop(1)
    unittest.main()