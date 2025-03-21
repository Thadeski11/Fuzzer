import aiohttp
import asyncio
import argparse
from requests.exceptions import RequestException
import time

parser = argparse.ArgumentParser(prog="Fuzzer", description="Script de fuzzing comum.")
parser.add_argument("-u", "--url", type=str, help="Passar a url alvo (Recomendado o uso de ' ').")
parser.add_argument("-w", "--wordlist", help="Passar a payload de testes.")
parser.add_argument("-t", "--time", type=int, default=1, help="Requests/Sec")
parser.add_argument("-o", "--output", help="Salva resultados em um arquivo.")
parser.add_argument("-s", "--scrapout", help="Salvar as urls [200] em um arquivo para possível scrap.")
args = parser.parse_args()


max_req_per_second = args.time
semaphore = asyncio.Semaphore(int(max_req_per_second))
async def fuzzing(session, url):
	async with semaphore:
		await asyncio.sleep(1)
		async with session.get(url, allow_redirects=False) as req:
			status_code = req.status
			html = await req.text()
			lenght = len(html)

			return url, status_code, lenght

async def main(wordlist):
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36"}
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
		rs = f"{url:<40} {status_code:>25} {lenght:>25}"
		print(rs)
		resultados.append(rs)
		if args.scrapout:
			if status_code == 200 or status_code == 302:
				with open(args.scrapout, "w") as scrap:
					scrap.write(url)
					scrap.write("\n")
	return resultados

def output(resultado, nome_arquivo):
		if nome_arquivo:
			with open(f"{nome_arquivo}", "w") as f:
				for i in resultado:
					f.write(i)
					f.write("\n")
		else:
			None


resultados = asyncio.run(main(args.wordlist))
output(resultados, args.output)
