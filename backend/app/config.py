# Database URL for SQLAlchemy (Currently using SQLite for local development)
DATABASE_URL = "sqlite:///./recipe_vault.db"


# JWT Configuration
SECRET_KEY = "gaKXwodtMdNcoydzbXPpLOdfa0GAP7f5dct2iVo99ofVdbZeLTFq0qU83GoNUsXulQEGdZlGlfUbg_sAUMvGKA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24*60  # 24 hours