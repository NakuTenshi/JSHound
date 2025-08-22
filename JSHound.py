import re 
import os
from yaspin import yaspin
from datetime import datetime
import requests 
import argparse
import time

# --- Argument Parsing ---
parser = argparse.ArgumentParser(
    description="JSHound: a tool for extacting js file from target and searchin intersting things on that files"
)

parser.add_argument("-d", required=True, type=str,
                    help="Target domain (e.g., example.com)")
parser.add_argument("-o", type=str,
                    help="Path to save the results")

args = parser.parse_args()
domain = args.d


# --- Colors ---
red     = "\033[31m"
blue    = "\033[34m"
green   = "\033[32m"
yellow = "\033[93m"
yellow_bg = "\033[43m"
name_bg = "\033[48;5;235m"
gray_bg = "\033[48;5;237m"
white_bg = "\033[47m"
reset   = "\033[0m"

def banner():
    os.system("clear")
    me = f"created by: " + name_bg + red + "NakuTenshi" + reset + reset
    banner = rf"""        
            {white_bg} {reset}                  {white_bg} {reset}                                     
           {white_bg } {reset}{yellow_bg} {reset}{white_bg} {reset}                {white_bg} {reset}{yellow_bg} {reset}{white_bg} {reset}                                     
          {white_bg} {reset}{yellow_bg}   {reset}{white_bg} {reset}              {white_bg} {reset}{yellow_bg}   {reset}{white_bg} {reset}                                  
         {white_bg}  {reset}{yellow_bg}    {reset}{white_bg} {reset}            {white_bg} {reset}{yellow_bg}    {reset}{white_bg}  {reset}                                   
        {white_bg}  {reset}{yellow_bg}      {reset}{white_bg}            {reset}{yellow_bg}      {reset}{white_bg}  {reset}                                  
       {white_bg}  {reset}{yellow_bg}                          {reset}{white_bg}  {reset}                                  
      {white_bg}  {reset}{yellow_bg}                            {reset}{white_bg}  {reset}                                 
     {white_bg}  {reset}{yellow_bg}                              {reset}{white_bg}  {reset}                                
    {white_bg}  {reset}{yellow_bg}                                {reset}{white_bg}  {reset}                               
   {white_bg}  {reset}{yellow_bg}                                  {reset}{white_bg}  {reset}                               
   {white_bg}  {reset}{yellow_bg}            {reset}{white_bg}    {reset}{yellow_bg}    {reset}{white_bg}       {reset}{yellow_bg}       {reset}{white_bg}  {reset}                               
   {white_bg}  {reset}{yellow_bg}            {reset}{white_bg}    {reset}{yellow_bg}   {reset}{white_bg}   {reset}{yellow_bg}            {reset}{white_bg}  {reset}                            
   {white_bg}  {reset}{yellow_bg}            {reset}{white_bg}    {reset}{yellow_bg}   {reset}{white_bg}   {reset}{yellow_bg}            {reset}{white_bg}  {reset}                               
   {white_bg}  {reset}{yellow_bg}            {reset}{white_bg}    {reset}{yellow_bg}    {reset}{white_bg}      {reset}{yellow_bg}        {reset}{white_bg}  {reset}                               
   {white_bg}  {reset}{yellow_bg}            {reset}{white_bg}    {reset}{yellow_bg}       {reset}{white_bg}     {reset}{yellow_bg}      {reset}{white_bg}  {reset} fuck this people                        
   {white_bg}  {reset}{yellow_bg}            {reset}{white_bg}    {reset}{yellow_bg}          {reset}{white_bg}   {reset}{yellow_bg}     {reset}{white_bg}  {reset} {me}                            
   {white_bg}  {reset}{yellow_bg}      {reset}{white_bg}          {reset}{yellow_bg}  {reset}{white_bg}          {reset}{yellow_bg}      {reset}{white_bg}  {reset}                               
    {white_bg}  {reset}{yellow_bg}                                {reset}{white_bg}  {reset}                               
    {white_bg}  {reset}{yellow_bg}                                {reset}{white_bg}  {reset}                                
      {white_bg}    {reset}{yellow_bg}                        {reset}{white_bg}    {reset}                                 
          {white_bg}    {reset}{yellow_bg}                {reset}{white_bg}    {reset}                                    
            {white_bg}    {reset}{yellow_bg}            {reset}{white_bg}    {reset}                                       
                {white_bg}    {reset}{yellow_bg}      {reset}{white_bg}    {reset}                                          
                    {white_bg}      {reset}                                  
"""
    print(banner)

def getFromCommonCrawl(domain:str, js_files:list) -> int:
    time.sleep(3)
    return 0


def getFromUrlscan(domain:str, js_files:list) -> int:
    return 0


def getFromWayback(domain:str, js_files:list) -> int:
    x = 0 
    # curentYear = datetime.now().year
    # response = requests.get("https://web.archive.org/cdx/search/cdx", params={
    #     "url": domain,
    #     "matchType": "domain",
    #     "fl": "timestamp,original",
    #     "collapse": "digest",
    #     "output": "json",
    #     "from": curentYear,
    #     "to": curentYear
    # })

    # if response.status_code == 200:
    #     snapshots = response.json()[1:]
    #     for snap in snapshots:
    #         url = snap[1]
    #         if url.endswith(".js") and url not in js_files:
    #             if not any(path in url for path in ["_nuxt"]):
    #                 x += 1
    #                 js_files.append(url)
    return x


def main():
    banner()

    print(f"<------------------ {yellow}Status{reset} ------------------>")
    print(f"{blue}[INFO]{reset} target: {red}{domain}{reset}")
    if args.o: print(f"{blue}[INFO]{reset} saving result at: {green}{args.o}{reset}")

    js_files = []

    print(f"\n<------------------- {yellow}Logs{reset} ------------------->")
    with yaspin(text=f"{yellow}sending request to archive.org{reset}", color="yellow") as sp:

        founded_js = getFromWayback(domain=domain, js_files=js_files)
        sp.write(f"{yellow}[+]{reset} got {founded_js} JS file from archive.org api")
        sp.text = f"{yellow}sending request to commomcrawl's api{reset}"

        founded_js = getFromCommonCrawl(domain=domain, js_files=js_files)
        sp.write(f"{yellow}[+]{reset} got {founded_js} JS file from commomcrawl's api")
        sp.text = f"{yellow}sending request to urlScan's api{reset}"

        founded_js = getFromUrlscan(domain=domain, js_files=js_files)
        sp.write(f"{yellow}[+]{reset} got {founded_js} JS file from urlScan's api")

        sp.text = f"{yellow}done.{reset}"
        sp.ok("✓")
    
    if js_files:
        print(js_files)
    else:
        pass


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(f"{red}[ERROR]{reset} No internet connection. Please check your network.")
        exit()
    except KeyboardInterrupt:
        print("\nbye :)")
        exit()
    except Exception as e:
        print(f"[{red}ERROR]{reset} there is an error: {e}")
        exit()