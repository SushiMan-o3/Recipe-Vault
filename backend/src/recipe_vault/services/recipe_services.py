import anthropic
import httpx
from bs4 import BeautifulSoup

from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

