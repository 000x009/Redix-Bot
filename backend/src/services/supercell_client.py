import aiohttp
from src.main.config import settings


class SupercellClient:
    def __init__(self):
        self.base_url = "https://api.brawlstars.com/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.BRAWL_STARS_API_KEY}"
        }

    async def verify_tag(self, tag: str) -> bool:
        try:
            cleaned_tag = tag.replace('#', '').upper()
            print(cleaned_tag)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/players/{cleaned_tag}",
                    headers=self.headers
                ) as response:
                    print(response, flush=True)
                    data = await response.json()
                    print(data, flush=True)
                    return response.status == 200
        except Exception as e:
            print(f"Error verifying tag: {e}", flush=True)
            return False

    def format_tag(self, tag: str) -> str:
        cleaned = tag.replace('#', '').replace(' ', '')
        return f"#{cleaned.upper()}"


client = SupercellClient()

async def main():
    tag = "#SDSDS1112"
    exists = await client.verify_tag(tag)
    if exists:
        print(f"Tag {tag} exists!")
    else:
        print(f"Tag {tag} does not exist")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
