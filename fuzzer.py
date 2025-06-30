import aiohttp
import asyncio
import argparse
import json

parser = argparse.ArgumentParser(prog="Fuzzer", description="Script de fuzzing comum.")
parser.add_argument("-u", "--url", type=str, help="Passar a url alvo (Recomendado o uso de ' ').")
parser.add_argument("-w", "--wordlist", help="Passar a payload de testes.")
parser.add_argument("-t", "--time", type=int, default=1, help="Requests/Sec")
parser.add_argument("-o", "--output", help="Salva resultados em um arquivo.")
parser.add_argument("-S", "--scrapout", help="Salvar as urls [200] em um arquivo para possível scrap.")
parser.add_argument("-H", "--headers", type=str, default=None, help=
'''Adiciona um ou mais headers para a request. Ex:
	Linux: >>> '{"Content-Type": "0"}' <<<
	Windows: >>> "{\"User-Agent\": \"test\"}" <<<
''')
args = parser.parse_args()


max_req_per_second = args.time
semaphore = asyncio.Semaphore(int(max_req_per_second))
async def fuzzing(session, url):
	async with semaphore:
		await asyncio.sleep(1)
		try:
			async with session.get(url, allow_redirects=False) as req:
				status_code = req.status
				html = await req.text()
				lenght = len(html)
				return url, status_code, lenght
		except asyncio.TimeoutError:
			await asyncio.sleep(3)
			return url, None, None
		except aiohttp.ClientError:
			return url, None, None
		except UnicodeDecodeError:
			print(f"Unicode error {url}")
			return url, None, None
	
async def main(wordlist, header):
	headers = header
	urls = []
	resultados = []
	with open(wordlist, "r") as w:
		for i in w:
			i = i.strip()
			url_true = args.url.replace("FUZZ", i)
			urls.append(url_true)

	async with aiohttp.ClientSession(headers=headers) as session:
		tasks = [fuzzing(session, url) for url in urls]
		results = await asyncio.gather(*tasks)

	for url, status_code, lenght in results:
		if status_code is not None and lenght is not None:
			rs = f"{url:<100} {status_code:>10} {lenght:>10}"
			print(rs)
			resultados.append(rs)
			if args.scrapout:
				if status_code == 200 or status_code == 302:
					with open(args.scrapout, "a") as scrap:
						scrap.write(url)
						scrap.write("\n")
	return resultados

def Output(resultado, nome_arquivo):
		if nome_arquivo:
			with open(f"{nome_arquivo}", "w") as f:
				for i in resultado:
					f.write(i)
					f.write("\n")
		else:
			None

def Headers(headers):
	if headers is None:
		return {"User-Agent": "{Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36}"}
	else:
		return json.loads(headers)


results_headers = Headers(args.headers)
results = asyncio.run(main(args.wordlist, results_headers))
Output(results, args.output)
