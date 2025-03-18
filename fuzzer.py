import requests
import argparse
from requests.exceptions import RequestException
import time
import threading
import queue

parser = argparse.ArgumentParser(prog="Fuzzer", description="Script de fuzzing comum.")
parser.add_argument("--url", required=True, help="Passar a url alvo (Recomendado o uso de ' ') Ex: 'https://google.com/FUZZ/?family=FUZZ'.")
parser.add_argument("--wordlist", required=True, help="Passar a payload de testes.")
parser.add_argument("--time", type=float, default=1, help="Para baixas taxas de requisição.")
parser.add_argument("--threads", type=int, help="Para altas taxas de requisição.")
parser.add_argument("--output", help="Salva resultados em um arquivo.")
args = parser.parse_args()

def escolha_arquivo_scrap():
	escolha_s_n = 0
	while True:
		urls_salvas = str(input("Caso queira guardar as URLs testadas em um arquivo, digite [S], caso não queira guardar digite [N]: ")).upper()
		if urls_salvas == "S":
			escolha_s_n = 0
			return escolha_s_n
			break
		elif urls_salvas == "N":
			escolha_s_n = 1
			return escolha_s_n
			break
		else:
			print("Escolha um valor válido...")
			time.sleep(0.5)
			continue

def fuzzing(url, resultado_queue=None):
	if args.threads:
		with semaforo:
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
			status_force = [429, 500]
		
			resposta = requests.get(url, headers=headers)
			status_code = resposta.status_code
			tamanho_pagina = len(resposta.text)
			resultado_formatado = f"{url:<40} {status_code:>25} {tamanho_pagina:>25}"  			

			print(resultado_formatado)
			if status_code in status_force:
				time.sleep(30)

			if resultado_queue is not None:
				resultado_queue.put((resultado_formatado))
			
			return resultado_formatado
	else:
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
		status_force = [429, 500]
		
		resposta = requests.get(url, headers=headers)
		status_code = resposta.status_code
		tamanho_pagina = len(resposta.text)
		resultado_formatado = f"{url:<40} {status_code:>25} {tamanho_pagina:>25}"  

		print(resultado_formatado)
		if status_code in status_force:
			time.sleep(30)

		return resultado_formatado, status_code

def fuzz_threading(wordlist):
	global semaforo
	semaforo = threading.Semaphore(args.threads)
	threads = []
	resultado_queue = queue.Queue()
	
	resultados = []

	for linhas in wordlist:
		try:
			linhas = linhas.strip()
			nova_url = args.url.replace("FUZZ", linhas)
			t = threading.Thread(target=fuzzing, args=(nova_url, resultado_queue, ))
			threads.append(t)
			t.start()
		except requests.exceptions.RequestException as e:
			print(f"Erro em [{nova_url}] : {e}")
			continue

	for t in threads:
		t.join()
	
	while not resultado_queue.empty():
		testes = resultado_queue.get()
		resultados.append(testes)


	return resultados

def fuzz_time(wordlist):
	escolha = escolha_arquivo_scrap()	
	
	status = 0
	resultados = []	
	if escolha == 0:
		arquivo_urls_nome = str(input("Digite o nome do arquivo: "))
		with open(arquivo_urls_nome, 'w') as arq:
			for linhas in wordlist:
				try: 
					linhas = linhas.strip()
					nova_url = args.url.replace("FUZZ", linhas)
					testes, status = fuzzing(nova_url)
					resultados.append(testes)
					if status == 200:
						arq.write(nova_url)
						arq.write("\n")
					time.sleep(args.time)
				except requests.exceptions.RequestException as e:
					print(f"Erro em [{nova_url}] : {e}")
					continue

	elif escolha == 1:
		for linhas in wordlist:
			try:
				linhas = linhas.strip()
				nova_url = args.url.replace("FUZZ", linhas)
				testes, status = fuzzing(nova_url)
				resultados.append(testes)
				time.sleep(args.time)
			except requests.exceptions.RequestException as e:
				print(f"Erro em [{nova_url}] : {e}")
				continue
	
	return resultados

with open(args.wordlist) as f:
	wordlist = f.readlines()

def output(resultado, nome_arquivo):
		if nome_arquivo:
			with open(f"{nome_arquivo}", "w") as f:
				for i in resultado:
					f.write(i)
					f.write("\n")
		else:
			None

if args.threads:
	resultados = fuzz_threading(wordlist)
	output(resultados, args.output)
else:
	resultados = fuzz_time(wordlist)
	output(resultados, args.output)
