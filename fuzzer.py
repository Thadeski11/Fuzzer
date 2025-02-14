import requests
import argparse
from ratelimit import limits, sleep_and_retry
from requests.exceptions import RequestException
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

parser = argparse.ArgumentParser(prog="Fuzzer", description="Script de fuzzing comum.")
parser.add_argument("--url", help="Passar a url alvo (Recomendado o uso de ' ').")
parser.add_argument("--wordlist", help="Passar a payload de testes.")
parser.add_argument("--time",  help="Passar o delay por segundo para cada requisição.")
args = parser.parse_args()

if args.time:
	None
else:
	args.time = 5

@sleep_and_retry
@limits(calls=int(args.time), period=1) 
def capturar_informacao(url):
	status_force = [429, 500, 502, 503, 504]
	with open(args.wordlist) as f:
		for i in f.readlines():
			linhas = i.replace("\n", "")
			try:
				nova_url = url.replace("FUZZ", linhas)
				resposta = requests.get(nova_url, headers=headers, timeout=10)

				status_code = resposta.status_code
				tamanho_pagina = len(resposta.text)
  
				print(f"{nova_url} -- STATUS {status_code}  -  LENGHT {tamanho_pagina}")
				if status_code in status_force:
					time.sleep(30)
    
			except requests.exceptions.RequestException as e:
				print(f"Erro na url [{nova_url}] : {e}")
				continue

 

capturar_informacao(args.url)
