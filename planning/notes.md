# 6/27/2026
## What i am thinking
- use a basic ETL (extract transform load) pipeline to essentially take raw data from PDFs using docling then transform it using anthropics api to then load it into the database for future use. i mean another idea i did have was i could possibly just create somehthing to clean the data myself but 
- probaby take the time to play around with docling tomorrow or the day out of tomorrow so I take a break from this project then figure out what docling is then come back to this project then write implement it on the small scale and code the pipeline
- was also thinking of making the ingredients and equipment for each recipe more complicated but then i realized the simpler it is the easier it is going to be for me to code and understand and there's sort of i guess less moving parts for me to mess up 

## Next Steps
- learn about docling and how it works
- get a basic frontend for login/register/logout + basic create and view all database working

# 6/26/2026
## What i am thinking
- so i wrote down all the login end points in auth.py and set up config.py where the secret key, hashing algorithm and how long it takes for the token to expire as well as the schemas using pydatic and the database model using sqlalchemy
- I also created some basic end points for the recipes itself, in particular, i created the create, delete, get all, get one recipe for the user. 
- Currently working on updating recipe but i am not really sure how i am going to make it work
- i have to design the pipeline for how the upload pdf, img, etc with docling works to then try encorperating it into recipes.py or maybe just create a new file for it then use claude tokens to filter then do stuff with it

## Next step
- design the pipeline for how the data will flow after doing upload file to creating recipes in the database
- learn about docling and how it works
- get a basic frontend for login/register/logout + basic create and view all database working


# 6/25/2026
## What I am thinking
- An online website made with react and fastApi that just stores a bunch of recipes for each user that it gets from pdfs, photos, docx, etc using docling (an open-source pdf extractor made by IBM), or websites using some sort of scraper maybe using beautifulSoup then using that raw data, we pass it into claude to organize the data (maybe put in $100 worth of tokens, which according to claude would last 65,000 recipes) then put it into a db where you can store and organize it. Also it would be easy to have a way to just manually add the recipes into the database.
- It would be nice to modify/delete/read the recipes, and be able to organize by date, title, length, etc

- Possibly later on, it would be good to see user profiles and all the receipes someone has public for others to see but thats a future though
- shoping list might be a nice additonal and a general planner for the next 7 days as well (significantly easier than profiles)

## Next steps:
- Design all the routes, the database (using ERD), API contract (request/response shapes, etc), and the general pipeline 
- Get a basic backend working with jwt authentication and manually adding the receipes and a very basic but simple frontend to it because login and authentication does not work with swagger

## In terms of tech stack
- FastAPI (backend) + React w typescript + axios for sending and recieving from backend (frontend)
- jwt tokens for login and authentication + hash password before storing and retriving for login
- sqlite for now -> PostgreSQL (+ SQLAlchemy)
- docling for reading photos, pdfs, etc and beautifulsoup for scraping the web

## Some basic resources
- https://www.geeksforgeeks.org/node-js/rest-api-introduction/
- https://youtu.be/SR5NYCdzKkc?si=0mJJhK47IOUiOo8B
- https://www.geeksforgeeks.org/html/what-is-axios/
- https://www.geeksforgeeks.org/web-tech/json-web-token-jwt/
- https://react.dev/learn
- https://platform.claude.com/docs/en/api/admin/api_keys/retrieve
tg
- https://www.geeksforgeeks.org/postgresql/postgresql-tutorial/