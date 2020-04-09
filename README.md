# Reed Job Seeker API Python Implementation
Small project with the goal of making a simple API wrapper from scratch for learning purposes. 
Picked Reed pretty much randomly

# Technical notes 
N.B. Seems like there's some sort of location locking on the API - pity as my lovely tests always get a 401
See https://www.reed.co.uk/developers/jobseeker 
Search Results output
{
    "results": [
        {
            "jobId": 40227781,
            "employerId": 563926,
            "employerName": "Modis",
            "employerProfileId": null,
            "employerProfileName": null,
            "jobTitle": "Development Manager  Deliver complex enterprise-scale software",
            "locationName": "Stoke-on-Trent",
            "minimumSalary": 50000.00,
            "maximumSalary": 60000.00,
            "currency": "GBP",
            "expirationDate": "12/05/2020",
            "date": "31/03/2020",
            "jobDescription": "blah blah ... ",
            "applications": 1,
            "jobUrl": "https://www.reed.co.uk/jobs/development-manager-deliver-complex-enterprise-scale-software/40227781"
        },
}

Details endpoint outputs
{
    "employerId": 0,
    "employerName": null,
    "jobId": 0,
    "jobTitle": null,
    "locationName": null,
    "minimumSalary": null,
    "maximumSalary": null,
    "yearlyMinimumSalary": null,
    "yearlyMaximumSalary": null,
    "currency": null,
    "salaryType": null,
    "salary": null,
    "datePosted": null,
    "expirationDate": null,
    "externalUrl": null,
    "jobUrl": null,
    "partTime": false,
    "fullTime": false,
    "contractType": null,
    "jobDescription": null,
    "applicationCount": 0
}
# Changes
### 0.1 
Initial commit, started implementing job searching functionality 

### 0.2
Basic function, no paging 

### 0.3 
Pretty happy with this now. Calling this the final version

### 0.4 
The real final, version, some fixes to try and get the tests passing here, no such luck, seems it's an API thing