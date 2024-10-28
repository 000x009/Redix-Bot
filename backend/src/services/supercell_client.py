import aiohttp

class SupercellClient:
    def __init__(self):
        self.base_url = "https://api.supercell.com"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def verify_tag(self, tag: str) -> bool:
        try:
            cleaned_tag = tag.replace('#', '').upper()
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/player/{cleaned_tag}",
                    headers=self.headers
                ) as response:
                    data = await response.json()
                    print(data)
                    return response.status == 200
        except Exception as e:
            print(f"Error verifying tag: {e}")
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
