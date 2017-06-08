# README #

Ranked API - A Backend platform for providing services to the Ranked Mobile apps.

### What is this repository for? ###

* Ranked API
* 0.1
* Django / Python

### How do I get set up? ###

* Dependencies:  Python 3.5 (will be 3.6 when AWS images catch up)

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