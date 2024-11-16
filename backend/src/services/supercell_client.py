import aiohttp
# from src.main.config import settings


class SupercellClient:
    def __init__(self):
        self.base_url = "https://api.brawlstars.com/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjAzZTdkNmY4LWNmYWQtNGQ2YS1iM2I2LTkxZDQxODdkMmE4ZSIsImlhdCI6MTczMTYwMTA5Nywic3ViIjoiZGV2ZWxvcGVyL2QwZTVjZmYzLTA0NjctZTUyNi1mYjUyLWZiMzA0MzljZjFhNyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMjEyLjUuMTU4LjE2Il0sInR5cGUiOiJjbGllbnQifV19.S6Mmz4_RIBIwzLzFE_dwxRCU6tLgSwhxNAAqJNcX14qMXHxhfvgNByhqY9ADRrTiWKiBRfzKiM2M8U1v3LIZRw"
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
                    print(response)

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
    tag = "#RPYJJJ2RY"
    exists = await client.verify_tag(tag)
    if exists:
        print(f"Tag {tag} exists!")
    else:
        print(f"Tag {tag} does not exist")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
