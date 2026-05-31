import aiohttp
import asyncio
import json

class Fuzzer():
	def __init__(self, url, wordlist, time=1, method='get', body=None, headers=None):
		self.url = url
		self.wordlist = wordlist
		self.time = time
		self.headers = headers
		self.method = method
		self.body = body
		self.semaphore = asyncio.Semaphore(int(self.time))


	async def fuzz_process(self, session, url, method, body=None):
		async with self.semaphore:
			await asyncio.sleep(1)
			try:
				if self.body is None:
					async with session.request(method, url, allow_redirects=True) as req:
						status_code = req.status
						html = await req.text()
						length = len(html)
						return url, status_code, length, None
				else:
					async with session.request(method, url, data=body, allow_redirects=True) as req:
						status_code = req.status
						html = await req.text()
						length = len(html)
						return url, status_code, length, body

			except asyncio.TimeoutError:
				await asyncio.sleep(3)
				return url, None, None, body
			except aiohttp.ClientError:
				return url, None, None, body
			except UnicodeDecodeError:
				return url, 200, "UNICODE_ERR", body
			except Exception as e:
				print(f"[ERROR] {type(e).__name__}: {e}")
				raise
	
	async def main_process(self):
		all_url = []
		all_body = []
		done_results = []
		with open(self.wordlist, "r") as w:
			if self.body is None:
				for lines in w:
					url = self.url.replace("FUZZ", lines.strip())
					all_url.append(url)
			else:
				for lines in w:
					url = self.url.replace("FUZZ", lines.strip())
					all_url.append(url)
					body = self.body.replace("FUZZ", lines.strip())
					all_body.append(body)
				
		async with aiohttp.ClientSession(headers=self.headers) as session:
			tasks = []
			if self.body is None:
				for url in all_url:
					tasks.append(self.fuzz_process(session, url, self.method))
			else:
				for url, data in zip(all_url, all_body):
					tasks.append(self.fuzz_process(session, url, self.method, data))
			url_results = await asyncio.gather(*tasks)

		if self.body is None:
			for url, status_code, length, _ in url_results:
				if status_code is not None and length is not None:
					print(f"{url:<100} {status_code:>10} {length:>10}")
					done_results.append({"url": url, "status_code": status_code, "length": length})
		else:
			for url, status_code, length, data in url_results:
				if status_code is not None and length is not None:
					print(f"{url:<100} {status_code:>10} {length:>10} {data:>20}")
					done_results.append({"url": url, "status_code": status_code, "length": length, "body": data})
		
		return done_results


	def headers(headers=None):
		if headers is None:
			return {"User-Agent": "{Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36}"}		
		else:
			return json.loads(headers)
