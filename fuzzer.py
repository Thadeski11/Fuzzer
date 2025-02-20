import requests
import argparse
from requests.exceptions import RequestException
import time
import threading

parser = argparse.ArgumentParser(prog="Fuzzer", description="Script de fuzzing comum.")
parser.add_argument("--url", help="Passar a url alvo (Recomendado o uso de ' ').")
parser.add_argument("--wordlist", help="Passar a payload de testes.")
parser.add_argument("--time", type=float, default=1, help="Para baixas taxas de requisição.")
parser.add_argument("--threads", type=int, help="Para altas taxas de requisição.")
args = parser.parse_args()

def fuzzing(url):
	if args.threads:
		with semaforo:
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
			status_force = [429, 500, 502, 503, 504]
		
			resposta = requests.get(url, headers=headers)
			status_code = resposta.status_code
			tamanho_pagina = len(resposta.text)
  
			print(f"{url} -- STATUS {status_code}  -  LENGHT {tamanho_pagina}")
			if status_code in status_force:
				time.sleep(30)
	else:
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
		status_force = [429, 500, 502, 503, 504]
		
		resposta = requests.get(url, headers=headers)
		status_code = resposta.status_code
		tamanho_pagina = len(resposta.text)
  
		print(f"{url} -- STATUS {status_code}  -  LENGHT {tamanho_pagina}")
		if status_code in status_force:
			time.sleep(30)
    

def fuzz_threading(wordlist):
	global semaforo
	semaforo = threading.Semaphore(args.threads)
	threads = []
	for linhas in wordlist:
		try:
			linhas = linhas.strip()
			nova_url = args.url.replace("FUZZ", linhas)
			t = threading.Thread(target=fuzzing, args=(nova_url,))
			threads.append(t)
			t.start()
		except requests.exceptions.RequestException as e:
			print(f"Erro em [{nova_url}] : {e}")
			continue
	for t in threads:
		t.join()

def fuzz_time(wordlist):
	for linhas in wordlist:
		try:
			linhas = linhas.strip()
			nova_url = args.url.replace("FUZZ", linhas)
			fuzzing(nova_url)
			time.sleep(args.time)
		except requests.exceptions.RequestException as e:
			print(f"Erro em [{nova_url}] : {e}")
			continue


with open(args.wordlist) as f:
	wordlist = f.readlines()


if args.threads:
	fuzz_threading(wordlist)
else:
	fuzz_time(wordlist)
