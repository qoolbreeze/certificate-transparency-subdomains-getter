#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author : qoolbreeze
# version 0.1

import re
import requests
from http import HTTPStatus
import sys
from argparse import ArgumentParser

def parse_args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain.")
    parser.add_argument('-o', '--output', type=str, help="path of the output file.")
    return parser.parse_args()

def clear_url(target:str) -> str:
    return re.sub('.*www\.','',target,1).split('/')[0].strip()

def save_subdomains(subdomain:str ,output_file:str) -> None:
    with open(output_file,"a") as f:
        f.write(subdomain + '\n')
        f.close()

def main():
    args = parse_args()

    subdomains = []
    target = clear_url(args.domain)
    output = args.output

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

    if req.status_code != HTTPStatus.OK:
        print("Can not join crt.sh") 
        sys.exit(1)

    for (key,value) in enumerate(req.json()):
        subdomains.append(value['name_value'])

    subdomains = sorted(set(subdomains))

    for subdomain in subdomains:
        print("[-]  {s}".format(s=subdomain))
        if output is not None:
            save_subdomains(subdomain,output)

if __name__ == "__main__":
    main()
