import re 
import os
from yaspin import yaspin
from datetime import datetime
import requests 
import argparse
import sys
import random
import time
from simple_term_menu import TerminalMenu

# --- init values ---
pathsForFilter = [
    "nuxt", 
    "jquery", 
    "bootstrap", 
    "react", 
    "vue", 
    "angular", 
    "polyfill", 
    "analytics", 
    "google-analytics", 
    "tagmanager", 
    "gtag", 
    "ads", 
    "adsense", 
    "doubleclick", 
    "facebook", 
    "twitter", 
    "linkedin", 
    "pinterest", 
    "hotjar", 
    "segment", 
    "sentry", 
    "datadog", 
    "newrelic", 
    "cloudflare", 
    "stripe", 
    "shopify", 
    "cdn", 
    "vendor", 
    "bundle", 
    "webpack", 
    "runtime", 
    "manifest",
    "highlight.min.js"
]
bannerTexts = [
        "fuck this people",
        "Knowledge is the real exploit.",
        "Curiosity is our weapon.",
        "Think like a hacker, act like a builder.",
        "Every bug is an opportunity.",
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
patterns = [
    r"aws_access_key", r"aws_secret_key", r"api key", r"passwd", r"pwd",
    r"heroku", r"slack", r"firebase", r"swagger", r"aws key", r"password",
    r"ftp password", r"jdbc", r"db", r"sql", r"secret jet", r"config",
    r"admin", r"json", r"gcp", r"htaccess", r"\.env", r"ssh key",
    r"\.git", r"access key", r"secret token", r"oauth_token",
    r"oauth_token_secret", r"smtp"
]
js_files = []
# regex = re.compile("|".join(patterns), re.IGNORECASE)
regex = re.compile(r"(aws_access_key|aws_secret_key|api[_-]?key|passwd|password|secret|.env|ssh key)", re.IGNORECASE)



# --- Argument Parsing ---
parser = argparse.ArgumentParser(
    description="JS Hound: a tool for extracting JavaScript files from a target and searching for interesting findings in those files."
)

parser.add_argument("-d", required=True, type=str,
                    help="Target domain (e.g., example.com)")
parser.add_argument("-pf", type=str,
                    help="path for drop (e.g., nuxt,node,jquery)")
parser.add_argument("-o", type=str,
                    help="Output path to save results")

args = parser.parse_args()
domain = args.d
if args.pf:
    pathsForFilter = args.pf.split(",")


# --- Colors ---
red     = "\033[31m"
blue    = "\033[34m"
green   = "\033[32m"
yellow  = "\033[93m"
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


def selectOptions(options:list) -> str:
    print(f"\n<------------- {yellow}Choose an option{reset} ------------->")

    menu = TerminalMenu(options,
                        menu_cursor_style=("fg_yellow","bold"),
                        menu_highlight_style=("fg_yellow",),
                        menu_cursor="> ",
                        )
    choice_index = menu.show()
    for _ in range(2):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
    sys.stdout.flush()

    selectedOption = str(options[choice_index]) 
    if selectedOption != "exit":
        return selectedOption
    else:
        print("\nbye :)")
        exit()


def getFromCommonCrawl(domain:str, js_files:list) -> int:
    time.sleep(5)
    return 0


def getFromUrlscan(domain:str, js_files:list) -> int:
    time.sleep(5)
    return 0


def getFromWayback(domain:str, js_files:list) -> int:
    x = 0 
    current_year = datetime.now().year
    response = requests.get("https://web.archive.org/cdx/search/cdx", params={
        "url": domain,
        "matchType": "domain",
        "fl": "timestamp,original",
        "collapse": "digest",
        "output": "json",
        "from": current_year,
        "to": current_year
    })

    if response.status_code == 200:
        snapshots = response.json()[1:]
        for snap in snapshots:
            url = snap[1]
            if url.endswith(".js") and url not in js_files:
                if not any(path in url for path in pathsForFilter):
                    x += 1
                    js_files.append(url)
    return x

def searchStuffInLocal(file_path):
    pass

def searchStuffOnline(url):
    response = requests.get(url)
    if response.status_code == 200:
        js_content = response.text
        for line_index,line in enumerate(js_content.splitlines(), 1):
            if regex.search(line):
                print(f"\n<----------------- {url} ----------------->")
                print(f"got something at line {line_index}")
                print(line)
                findStuff += 1


def main():
    banner()

    print(f"<------------------ {yellow}Status{reset} ------------------>")
    print(f"{blue}[INFO]{reset} Target: {red}{domain}{reset}")
    if args.o: print(f"{blue}[INFO]{reset} Saving results to: {green}{args.o}{reset}")
    if len(pathsForFilter) > 5:
        print(f"{blue}[INFO]{reset} Paths to skip: {', '.join(pathsForFilter[:5])}, ... (+{len(pathsForFilter)-5} more)")
    else:
        print(f"{blue}[INFO]{reset} Paths to skip: {', '.join(pathsForFilter)}{reset}")




    selectedOption = selectOptions([
        "Find the target's JS files and search for interesting stuff in them",
        "Find interesting stuff in local JS files",
        "exit"
    ])

    if selectedOption == "Find the target's JS files and search for interesting stuff in them":
        print(f"\n<------------------- {yellow}Logs{reset} ------------------->")
        with yaspin(text=f"{yellow}Sending a request to the Archive.org API{reset}", color="yellow") as sp:

            founded_js = getFromWayback(domain=domain, js_files=js_files)
            sp.write(f"{yellow}[+]{reset} Got {founded_js} JS file(s) from the Archive.org API")
            sp.text = f"{yellow}Sending a request to the Common Crawl API{reset}"

            founded_js = getFromCommonCrawl(domain=domain, js_files=js_files)
            sp.write(f"{yellow}[+]{reset} Got {founded_js} JS file(s) from the Common Crawl API")
            sp.text = f"{yellow}Sending a request to the urlscan.io API{reset}"

            founded_js = getFromUrlscan(domain=domain, js_files=js_files)
            sp.write(f"{yellow}[+]{reset} Got {founded_js} JS file(s) from the urlscan.io API")

            sp.text = f"{yellow}Done.{reset}"
            sp.ok("✓")
        
        if js_files:
            print(f"{blue}[INFO]{reset} Found {red}{len(js_files)}{reset} JS file(s)")

            selectedOption = selectOptions([
                                            "do you want to search for interesting stuff in online (slower method)",
                                            "do you want to download the js files in local then search for interresting stuff at local (faster method)"
                                            ])
            
            if selectedOption == "do you want to search for interesting stuff in online (slower method)":
                findStuff = 0

                for url in js_files:
                    searchStuffOnline(url)
                if findStuff: 
                    print(f"{blue}[INFO]{reset} {red}{findStuff}{reset} things found.\nQuitting...")
                    exit()
                else:
                    print("Nothing found :(\nQuitting...")
                    exit()

            else:
                pass
        else:
            print("Nothing found :(\nQuitting...")
            exit()

        
    else:
        pass
    

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(f"{red}[ERROR]{reset} No internet connection. Please check your network.")
        exit()
    except KeyboardInterrupt:
        print("\nBye :)")
        exit()
    except Exception as e:
        print(f"[{red}ERROR]{reset} An error occurred: {e}")
        exit()
