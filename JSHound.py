import re 
import os
from yaspin import yaspin
from datetime import datetime
import requests 
import argparse
import random
import time

# --- init values ---
pathsForFilter = ["nuxt"]
bannerTexts = [
        "fuck this people",
        "Knowledge is the real exploit.",
        "Curiosity is our weapon.",
        "Think like a hacker, act like a builder.",
        "Every bug is an opportunity.",
        "Hack the system, not the people.",
        "Code is temporary, mindset is permanent.",
        "Access is earned, not given.",
        "Break assumptions, not ethics.",
        "Read the source, change the world.",
        "The best payload is persistence.",
        "Trust nothing, verify everything.",
        "Map the attack surface, master the craft.",
        "Skill > tools, always.",
        "From 404s to breakthroughs.",
        "Rules are interfaces—learn their edges.",
        "Small scripts, big impact.",
        "Signal over noise, always.",
        "Think adversarial, build responsibly.",
        "Exploit curiosity, patch ignorance.",
        "Velocity comes from clarity.",
        "Errors are roadmaps, not obstacles.",
        "Every system hides a story.",
        "Obscurity is fragile security.",
        "What you patch today saves you tomorrow.",
        "Recon is half the battle.",
        "A true hacker never stops learning.",
        "Data is the new zero-day.",
        "Good hackers break barriers, not laws.",
        "Every request tells a secret.",
        "The shell is just the beginning.",
        "Creativity beats automation.",
        "Knowledge shared is power multiplied.",
        "Strong security is invisible.",
        "A hacker sees patterns where others see noise.",
        "Silence is stealth, noise is failure.",
        "Curiosity cracks the strongest locks.",
        "The deepest bugs live in plain sight.",
        "Persistence is the ultimate exploit.",
        "Hackers don’t wait for permission.",
        "Adapt, exploit, evolve."
    ]


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
black_bg = "\033[40m"
white_bg = "\033[47m"
reset   = "\033[0m"

def banner():
    os.system("clear")
    choiced_text = random.choice(bannerTexts)

    me = f"created by: " + name_bg + red + "NakuTenshi" + reset + reset
    banner = rf"""        
           {black_bg} {reset}                   {black_bg} {reset}                                     
          {black_bg } {reset}{yellow_bg} {reset}{black_bg} {reset}                 {black_bg} {reset}{yellow_bg} {reset}{black_bg} {reset}                                     
         {black_bg} {reset}{yellow_bg}   {reset}{black_bg} {reset}               {black_bg} {reset}{yellow_bg}   {reset}{black_bg} {reset}                                  
        {black_bg}  {reset}{yellow_bg}    {reset}{black_bg} {reset}             {black_bg} {reset}{yellow_bg}    {reset}{black_bg}  {reset}                                   
       {black_bg}  {reset}{yellow_bg}      {reset}{black_bg}             {reset}{yellow_bg}      {reset}{black_bg}  {reset}                                  
      {black_bg}  {reset}{yellow_bg}                           {reset}{black_bg}  {reset}                                  
     {black_bg}  {reset}{yellow_bg}                             {reset}{black_bg}  {reset}                                 
    {black_bg}  {reset}{yellow_bg}                               {reset}{black_bg}  {reset}                                
   {black_bg}  {reset}{yellow_bg}                                 {reset}{black_bg}  {reset}                               
   {black_bg}  {reset}{yellow_bg}                                 {reset}{black_bg}  {reset} 
   {black_bg}  {reset}{yellow_bg}           {reset}{black_bg}   {reset}{yellow_bg}    {reset}{black_bg}         {reset}{yellow_bg}      {reset}{black_bg}  {reset}                      
   {black_bg}  {reset}{yellow_bg}           {reset}{black_bg}   {reset}{yellow_bg}   {reset}{black_bg}   {reset}{yellow_bg}             {reset}{black_bg}  {reset}               
   {black_bg}  {reset}{yellow_bg}           {reset}{black_bg}   {reset}{yellow_bg}   {reset}{black_bg}   {reset}{yellow_bg}             {reset}{black_bg}  {reset}                               
   {black_bg}  {reset}{yellow_bg}           {reset}{black_bg}   {reset}{yellow_bg}    {reset}{black_bg}      {reset}{yellow_bg}         {reset}{black_bg}  {reset}                               
   {black_bg}  {reset}{yellow_bg}           {reset}{black_bg}   {reset}{yellow_bg}       {reset}{black_bg}     {reset}{yellow_bg}       {reset}{black_bg}  {reset}                         
   {black_bg}  {reset}{yellow_bg}           {reset}{black_bg}   {reset}{yellow_bg}          {reset}{black_bg}   {reset}{yellow_bg}      {reset}{black_bg}  {reset}      
   {black_bg}  {reset}{yellow_bg}     {reset}{black_bg}        {reset}{yellow_bg}    {reset}{black_bg}         {reset}{yellow_bg}       {reset}{black_bg}  {reset}                               
   {black_bg}  {reset}{yellow_bg}                                 {reset}{black_bg}  {reset}                               
   {black_bg}  {reset}{yellow_bg}                                 {reset}{black_bg}  {reset}                                
    {black_bg}    {reset}{yellow_bg}                           {reset}{black_bg}    {reset}                                 
      {black_bg}    {reset}{yellow_bg}                       {reset}{black_bg}    {reset}                                    
        {black_bg}    {reset}{yellow_bg}                   {reset}{black_bg}    {reset}                                       
          {black_bg}    {reset}{yellow_bg}               {reset}{black_bg}    {reset}   "{choiced_text}"                                        
              {black_bg}               {reset}        {me}
"""                 
    print(banner)

def getFromCommonCrawl(domain:str, js_files:list) -> int:
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
    #             if not any(path in url for path in pathsForFilter):
    #                 x += 1
    #                 js_files.append(url)
    return x


def main():
    banner()

    print(f"<------------------ {yellow}Status{reset} ------------------>")
    print(f"{blue}[INFO]{reset} target: {red}{domain}{reset}")
    if args.o: print(f"{blue}[INFO]{reset} saving result at: {green}{args.o}{reset}")
    print(f"{blue}[INFO]{reset} Paths for Drop: {red}{pathsForFilter}{reset}")

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
