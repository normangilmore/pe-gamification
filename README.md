# pe-gamification
Tools for tracking Public Editor volunteer and project stats.

## Notes from Fall '20 Gamification Subteam
  - `event_model` contains our database model and insert/query tools
  - `pybossa_api` contains pythons scripts that pull data from https://pe.goodlylabs.org/ using the Pybossa API
  - In Fall 2020 we designed a database and filled it with user/taskrun data from projects in the [covidarticles](https://pe.goodlylabs.org/project/category/covidarticles/) and [covidtrainingtasks](https://pe.goodlylabs.org/project/category/covidtrainingtasks/) categories of Public Editor. We also defined an initial set of badges (see `badge_list.csv`) and added users who are owed these badges into the EmailCandidate table (see `event_model/query_badge.py)`. 
  - We are very close to finishing version one of the gamification system; we need to insert the appropriate Sengrid information into our database and write a python script to query the email candidates along with the Sengrid email ID, then send out these emails. 

