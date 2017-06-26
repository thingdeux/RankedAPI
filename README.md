# README #

Ranked API - A Backend platform for providing services to the Ranked Mobile apps.

### What is this repository for? ###

This repository holds the backend API for GoRanked.com. For complete functionality during development
you will need access to AWS credentials for our S3 Video Uploads buckets.  Please contact
Josh (me@josh.land) for details.


### How do I get set up? ###

* Dependencies:  Python 3.5 (will be 3.6 when AWS images catch up)

* PreRequisites: 
    - Credentials need to be setup in ~/.aws/credentials for the S3 buckets.  Not storing them in the repo.

* Installing:
    - run pip(3) -r requirements.txt
    - run manage.py migrate to setup the DB.


### Structure

    /docs - Various documentation (API / Notes / TODOS / Useful)
    /conf - Configuration files for deployed services (nginx / bash..etc)
    /scripts - Bash Scripts for deployed services
    /src - Python / Django Source Code
    /static - Any Static Files
    /templates - Django Templates
    
### Contribution guidelines ###

* PEP8 or bust! *(Exceptions where applicable)*
* Simple, Yeah....Simple.  
* Clarity is better than brevity.
* Use Re-Usable Abstract Mixins for Django Modelling where possible (multiple examples in codebase)
* Comments should convey developer thoughts or reasons - not simply parrot what's happening below.
* Inline comments should be used sparingly - comment above your code.
* TDD isn't a must but you *should* have tests for any significant functionality. "Not enough time" won't be an acceptable excuse.
* Test cases should not have dependencies - http or otherwise. Mock where necessary.