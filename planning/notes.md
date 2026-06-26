# What I am thinking - 6/25/2026
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