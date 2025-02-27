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
			status_force = [429, 500]
		
			resposta = requests.get(url, headers=headers)
			status_code = resposta.status_code
			tamanho_pagina = len(resposta.text)
  
			print(f"{url} -- STATUS {status_code}  -  LENGHT {tamanho_pagina}")
			if status_code in status_force:
				time.sleep(30)
			
	else:
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
		status_force = [429, 500]
		
		resposta = requests.get(url, headers=headers)
		status_code = resposta.status_code
		tamanho_pagina = len(resposta.text)
  
		print(f"{url} -- STATUS {status_code}  -  LENGHT {tamanho_pagina}")
		if status_code in status_force:
			time.sleep(30)
    

def fuzz_threading(wordlist):
	escolha_s_n = []
	while True:
		urls_salvas = str(input("Caso queira guardar as URLs testadas em um arquivo, digite [S] para concordar ou [N] para não concordar: ")).upper()
		if urls_salvas == "S":
			escolha_s_n.append(0)
			arquivo_urls_nome = str(input("Digite o nome do arquivo: "))
			break
		elif urls_salvas == "N":
			escolha_s_n.append(1)
			break
		else:
			print("Escolha um valor válido...")
			time.sleep(0.5)
			continue

	global semaforo
	semaforo = threading.Semaphore(args.threads)
	threads = []
	if escolha_s_n[0] == 0:
		with open(arquivo_urls_nome, 'w') as arq:
			for linhas in wordlist:
				try: 
					linhas = linhas.strip()
					nova_url = args.url.replace("FUZZ", linhas)
					arq.write(nova_url)
					arq.write("\n")
					t = threading.Thread(target=fuzzing, args=(nova_url,))
					threads.append(t)
					t.start()
		
				except requests.exceptions.RequestException as e:
					print(f"Erro em [{nova_url}] : {e}")
					continue
	elif escolha_s_n[1] == 1:
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
	escolha_s_n = []
	while True:
		urls_salvas = str(input("Caso queira guardar as URLs testadas em um arquivo, digite [S] para concordar ou [N] para não concordar: ")).upper()
		if urls_salvas == "S":
			escolha_s_n.append(0)
			arquivo_urls_nome = str(input("Digite o nome do arquivo: "))
			break
		elif urls_salvas == "N":
			escolha_s_n.append(1)
			break
		else:
			print("Escolha um valor válido...")
			time.sleep(0.5)
			continue
		
	if escolha_s_n[0] == 0:
		with open(arquivo_urls_nome, 'w') as arq:
			for linhas in wordlist:
				try: 
					linhas = linhas.strip()
					nova_url = args.url.replace("FUZZ", linhas)
					arq.write(nova_url)
					arq.write("\n")
					fuzzing(nova_url)
					time.sleep(args.time)
				except requests.exceptions.RequestException as e:
					print(f"Erro em [{nova_url}] : {e}")
					continue
	elif escolha_s_n[1] == 1:
		for linhas in wordlist:
			try:
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
