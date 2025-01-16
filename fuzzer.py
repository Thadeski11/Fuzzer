import requests
import argparse
from requests_ratelimiter import LimiterSession
from time import time

parser = argparse.ArgumentParser(prog="Fuzzer", description="Script de fuzzing comum.")
parser.add_argument("--url", help="Passar a url alvo.")
parser.add_argument("--wordlist", help="Passar a payload de testes.")
parser.add_argument("--time",  help="Passar o delay por segundo para cada requisição.")
args = parser.parse_args()


#Argumentos
arquivo_wordlist = args.wordlist
url_alvo = args.url
tempo_req = args.time


abrir_arquivo = open(f'{arquivo_wordlist}', 'r')

#Lista da wordlist
arquivo_completo = []

#Função de preparação para payload
def preparar_wordlist(wordlist):
 linhas_do_arquivo_n = []

 for linha in wordlist:
  linhas_do_arquivo_n.append(linha)

 linhas_do_arquivo = [linhas[:-1] for linhas in linhas_do_arquivo_n]
 for linha in linhas_do_arquivo:
  arquivo_completo.append(linha) 

#Executa função para montar lista da wordlist
preparar_wordlist(abrir_arquivo) 


#Trata requisição por segundo
session = LimiterSession(per_second=int(tempo_req))
start = time()

#Executa o script na url 
def capturar_informacao(url):
 for linhas in arquivo_completo:
  nova_url = url.replace("FUZZ", linhas) 
  resposta = session.get(nova_url)

  status_code = resposta.status_code
  tamanho_pagina = len(resposta.text)

  time()
  
  
  print(f"{nova_url} -- STATUS {status_code}  -  LENGHT {tamanho_pagina}")

 

capturar_informacao(url_alvo)

