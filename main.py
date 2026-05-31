from core.fuzzer import Fuzzer
from core.output import Output
import asyncio
import argparse

parser = argparse.ArgumentParser(prog="Fuzzer", description="")
parser.add_argument("-u", "--url", type=str, required=True, help="Passar a url alvo (Recomendado o uso de ' ').")
parser.add_argument("-w", "--wordlist", required=True, help="Passar a payload de testes.")
parser.add_argument("-t", "--time", type=int, default=1, help="Requests/Sec")
parser.add_argument("-X", "--method", type=str, default="get", help="Definir protocolo HTTP.")
parser.add_argument("-D", "--data", type=str, default=None, help=
'''Adiciona dados ao corpo da request. Formats:
	application/x-www-form-urlencoded >>> 'user=test'
	application/json >>> '{"hs":"1"}'
''')
parser.add_argument("-H", "--headers", type=str, default=None, help=
'''Adiciona um ou mais headers para a request. Formats:
	Linux: >>> '{"Content-Type": "0"}' <<<
	Windows: >>> "{\"User-Agent\": \"test\"}" <<<
''')
parser.add_argument("-ot", "--output-txt", help="Exporta resultados para um arquivo TXT.")
parser.add_argument("-oj", "--output-json", help="Exporta resultados para um arquivo JSON.")
parser.add_argument("-ox", "--output-xml", help="Exporta resultados para um arquivo XML.")
parser.add_argument("-oc", "--output-csv", help="Exporta resultados para um arquivo CSV.")
args = parser.parse_args()

def main():
	headers = Fuzzer.headers(args.headers)
	fuzzing = Fuzzer(args.url, args.wordlist, args.time, args.method, args.data, headers)
	results = asyncio.run(fuzzing.main_process())
	
	if args.output_txt:
		output = Output(results, args.output_txt)
		output.text_file()

	if args.output_json:
		output = Output(results, args.output_json)
		output.json_file()

	if args.output_xml:
		output = Output(results, args.output_xml)
		output.xml_file()

	if args.output_csv:
		output = Output(results, args.output_csv)
		output.csv_file()


if __name__ == "__main__":
	main() 
