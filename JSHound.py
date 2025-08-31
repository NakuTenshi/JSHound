import re 
import os
from yaspin import yaspin
from datetime import datetime
import requests 
import argparse
import sys
import json
import random
import time
from simple_term_menu import TerminalMenu
import urllib3

# disable SSL warnings if using verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Argument Parsing ---
parser = argparse.ArgumentParser(
    description="JS Hound: a tool for extracting JavaScript files from a target and searching for interesting findings in those files."
)

parser.add_argument("-d", required=True, type=str, help="Target domain (e.g., example.com)")

parser.add_argument("-fp", type=str, help="Comma-separated list of paths to filter (e.g., nuxt,node,jquery)")
parser.add_argument("-w_fp", type=str, help="Wordlist file containing paths to filter (e.g., ./pathskip.txt)")

parser.add_argument("-p", type=str, help="Comma-separated list of patterns to search for (e.g., password,api_key,autotoken,token)")
parser.add_argument("-w_p", type=str, help="Wordlist file containing patterns to search for (e.g., ./patterns.txt)")


# --- init values ---
pathsForFilter = [
    "nuxt", "jquery", "bootstrap",
    "react", "vue", "angular",
    "polyfill", "analytics", "google-analytics",
    "tagmanager", "gtag", "ads",
    "adsense", "doubleclick", "facebook",
    "twitter", "linkedin", "pinterest",
    "hotjar", "segment", "sentry",
    "datadog", "newrelic", "cloudflare",
    "stripe", "shopify", "cdn",
    "vendor", "bundle", "webpack",
    "runtime", "manifest", "highlight.min.js"
]

bannerTexts = [
    "fuck this people", "Knowledge is the real exploit.", "Curiosity is our weapon.",
    "Think like a hacker, act like a builder.", "Every bug is an opportunity.", "Code is temporary, mindset is permanent.",
    "Access is earned, not given.", "Break assumptions, not ethics.", "Read the source, change the world.",
    "The best payload is persistence.", "Trust nothing, verify everything.", "Map the attack surface, master the craft.",
    "Skill > tools, always.", "From 404s to breakthroughs.", "Rules are interfaces—learn their edges.",
    "Small scripts, big impact.", "Signal over noise, always.", "Think adversarial, build responsibly.",
    "Exploit curiosity, patch ignorance.", "Velocity comes from clarity.", "Errors are roadmaps, not obstacles.",
    "Every system hides a story.", "Obscurity is fragile security.", "What you patch today saves you tomorrow.",
    "Recon is half the battle.", "A true hacker never stops learning.", "Data is the new zero-day.",
    "Good hackers break barriers, not laws.", "Every request tells a secret.", "The shell is just the beginning.",
    "Creativity beats automation.", "Knowledge shared is power multiplied.", "Strong security is invisible.",
    "A hacker sees patterns where others see noise.", "Silence is stealth, noise is failure.", "Curiosity cracks the strongest locks.",
    "The deepest bugs live in plain sight.", "Persistence is the ultimate exploit.", "Hackers don’t wait for permission.",
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


args = parser.parse_args()
domain = args.d


if args.fp and not args.w_fp:
    pathsForFilter = str(args.fp).split(",")
elif args.w_fp and not args.fp:
    wordlist_path = args.w_fp
    if os.path.exists(wordlist_path):
        with open(wordlist_path , 'r') as file:
            pathsForFilter = file.read().splitlines()
    else:
        print(f"{red}[ERROR]{reset} the wordlist doesn't exists")
        exit()

if args.p and not args.w_p:
    patterns = str(args.p).split(",") 
elif args.w_p and not args.p:
    wordlist_path = args.w_p
    if os.path.exists(wordlist_path):
        with open(wordlist_path , 'r') as file:
            patterns = file.read().splitlines()
    else:
        print(f"{red}[ERROR]{reset} the wordlist doesn't exists")
        exit()


target_result_folder = f"./targets/{domain}/result/"
target_jsFiles_folder = f"./targets/{domain}/jsFiles/"
target_result_file = os.path.join(target_result_folder, "result.txt")

os.makedirs(target_result_folder,exist_ok=True)

js_files = []
regex = re.compile("|".join(patterns), re.IGNORECASE)
findings_count = 0


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

def getFromWayback(domain:str, js_files:list, sp) -> int:
    try:
        x = 0 
        current_year = datetime.now().year
        response = requests.get("https://web.archive.org/cdx/search/cdx", params={
            "url": domain,
            "matchType": "domain",
            "fl": "original",
            "collapse": "digest",
            "from": current_year,
            "to": current_year
        }, stream=True)

        if response.status_code == 200:
            for url in response.iter_lines():
                if url:
                    url = url.decode("utf-8")
                    if url.endswith(".js") and not any(path in url for path in pathsForFilter):
                        x += 1
                        js_files.append(url)
        return x
    except requests.exceptions.ConnectionError:
        sp.write(f"{red}[-]{reset} Couldn't get data from Archive.org API")


def getFromCommonCrawl(domain:str, js_files:list, sp) -> int:
    try:
        x = 0 
        currentTimeResponse = requests.get("https://index.commoncrawl.org/collinfo.json")
        if currentTimeResponse.status_code == 200:
            currentTime = currentTimeResponse.json()[0]["id"]

            response = requests.get(f"https://index.commoncrawl.org/{currentTime}-index?url=*.{domain}/*&output=json&collapse=urlkey")
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        url = str(data["url"])
                        if url.endswith(".js") and not any(path in url for path in pathsForFilter):
                            js_files.append(url)
                            x += 1
                            
        return x
    except requests.exceptions.ConnectionError:
        sp.write(f"{red}[-]{reset} Couldn't get data from Common Crawl API")

def getFromUrlscan(domain:str, js_files:list, sp) -> int:
    try:
        x = 0
        domainRegex = re.compile(rf"^https?://([a-zA-Z0-9-]+\.)*{re.escape(domain)}(/|$)")
        getResultResponse = requests.get(f"https://urlscan.io/api/v1/search/?q=domain:{domain}")
        
        if getResultResponse.status_code == 200:
            results = getResultResponse.json()["results"]

            for i in results:
                resultDomain = i["task"]["domain"]
                if resultDomain == domain:
                    resultUrl = i["result"]
                    break

            resultResponse = requests.get(resultUrl) 
            if resultResponse.status_code == 200:
                listUrls = [url for url in resultResponse.json()["lists"]["urls"] if str(url).endswith('.js')]
                for url in listUrls:
                    if not any(path in url for path in pathsForFilter):
                        if domainRegex.search(url):
                            js_files.append(url)
                            x += 1 

        return x 
    except requests.exceptions.ConnectionError:
        sp.write(f"{red}[-]{reset} Couldn't get data from urlscan.io API")

def downloadJsFiles(js_files:list , sp):
    global jsFolder_path

    os.makedirs(target_jsFiles_folder , exist_ok=True)

    for url in js_files:
        sp.text = f"preparing to downlaod {url}..."

        jsFile_url = "/".join(url.split("/")[3:])
        jsFolder_url = "/".join(jsFile_url.split("/")[:-1])

        jsFolder_path = os.path.join(target_jsFiles_folder,jsFolder_url)
        jsFiles_path = os.path.join(target_jsFiles_folder, jsFile_url)


        response = requests.get(url, stream=True, verify=False)
        if response.status_code == 200:
            total = int(response.headers.get("content-length", 0))
            downloaded = 0


            os.makedirs(jsFolder_path , exist_ok=True)
            with open(jsFiles_path, "wb") as f:
                start_time = time.time()
                for chunk in response.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed / 1024  # KB/s

                        if total > 0:
                            percent = (downloaded / total) * 100
                            sp.text = f"{yellow}[+]{reset} downloading {url} {percent:.2f}% ({speed:.1f} KB/s)"
                        else:
                            sp.text = f"{yellow}[+]{reset} downloading {url} {downloaded/1024:.1f} KB ({speed:.1f} KB/s)"
                sp.write(f"{yellow}[*]{reset} {jsFile_url} downloaded")
    return jsFolder_path

def searchStuffInLocal(folder_path, sp):
    global findings_count

    js_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
    
    for js_file in js_files:
        with open(js_file, "r", encoding="utf-8", errors="ignore") as file:
            for line_index, line in enumerate(file , 1):
                match = regex.search(line)
                if match:
                    matchWord = f"{red}{match.group()}{reset}"
                    sp.write(f"{yellow}[+]{reset} got '{matchWord}' at line {red}{line_index}{reset} from '{red}{js_file}{reset}'")

                    with open(target_result_file , "a") as file:
                        content = ""
                        content += f"\n<----------------- {js_file} ----------------->\n"
                        content += f"Match: '{match.group()}' Line: {line_index}\n"
                        content += f"{line}\n"
                        file.write(content)
                        
                        findings_count += 1
    if findings_count: 
        sp.write(f"{yellow}[+]{reset} got {red}{findings_count}{reset} stuff")                        
        sp.write(f"{yellow}[+]{reset} saving result at: {blue}{target_result_file}{reset}")                        

        sp.text = f"{yellow}Done.{reset}"
        sp.ok("✓")
        exit()
    else:
        sp.write(f"{yellow}[*]{reset} Nothing found :(\nQuitting...")
        exit()

def searchStuffOnline(js_files, sp):
    global findings_count, jsFolder_path

    for url in js_files:
        sp.text = f"{yellow}sending request to {url}{reset}"
        response = requests.get(url)
        if response.status_code == 200:
            sp.text = f"{yellow}trying to extract staff...{reset}"
            js_content = response.text

            for line_index,line in enumerate(js_content.splitlines(), 1):
                match = regex.search(line) 
                if match:
                    matchWord = f"{red}{match.group()}{reset}"
                    sp.write(f"{yellow}[+]{reset} got '{matchWord}' at line {red}{line_index}{reset} from '{red}{url}{reset}'")

                    with open(target_result_file , "a") as file:
                        content = ""
                        content += f"\n<----------------- {url} ----------------->\n"
                        content += f"Match: '{match.group()}' Line: {line_index}\n"
                        content += f"{line}\n"
                        file.write(content)
                        
                        findings_count += 1
    if findings_count: 
        sp.write(f"{yellow}[+]{reset} got {red}{findings_count}{reset} stuff")                        
        sp.write(f"{yellow}[+]{reset} saving result at: {blue}{target_result_file}{reset}")                        

        sp.text = f"{yellow}Done.{reset}"
        sp.ok("✓")
        exit()
    else:
        sp.write(f"{yellow}[*]{reset} Nothing found :(\nQuitting...")
        exit()






def main():
    global js_files
    banner()

    print(f"<------------------ {yellow}Status{reset} ------------------>")
    print(f"{blue}[INFO]{reset} Target: {red}{domain}{reset}")
    if len(pathsForFilter) > 5:
        print(f"{blue}[INFO]{reset} Paths to skip: {', '.join(pathsForFilter[:5])}, ... (+{len(pathsForFilter)-5} more)")
    else:
        print(f"{blue}[INFO]{reset} Paths to skip: {', '.join(pathsForFilter)}{reset}")
    if len(patterns) > 5:
        print(f"{blue}[INFO]{reset} Patterns to find: {', '.join(patterns[:5])}, ... (+{len(patterns)-5} more)")
    else:
        print(f"{blue}[INFO]{reset} Patterns to find: {', '.join(patterns)}{reset}")



    selectedOption = selectOptions([
        "Find the target's JS files and search for interesting stuff in them",
        "Find interesting stuff in local JS files",
        "exit"
    ])

    if selectedOption == "Find the target's JS files and search for interesting stuff in them":
        print(f"\n<------------------- {yellow}Logs{reset} ------------------->")
        with yaspin(text=f"{yellow}Sending a request to the Archive.org API{reset}", color="yellow") as sp:

            founded_js = getFromWayback(domain=domain, js_files=js_files, sp=sp)
            if founded_js: sp.write(f"{yellow}[+]{reset} Got {red}{founded_js}{reset} JS file(s) from Archive.org API")
            sp.text = f"{yellow}Sending a request to the Common Crawl API{reset}"

            founded_js = getFromCommonCrawl(domain=domain, js_files=js_files, sp=sp)
            if founded_js: sp.write(f"{yellow}[+]{reset} Got {red}{founded_js}{reset} JS file(s) from Common Crawl API")
            sp.text = f"{yellow}Sending a request to the urlscan.io API{reset}"

            founded_js = getFromUrlscan(domain=domain, js_files=js_files, sp=sp)
            if founded_js:  sp.write(f"{yellow}[+]{reset} Got {red}{founded_js}{reset} JS file(s) from urlscan.io API")

        
        if js_files:
            print(f"{yellow}[+]{reset} Sorting JS file(s)")
            js_files = sorted(set(js_files))
            print(f"{yellow}[+]{reset} Found {red}{len(js_files)}{reset} JS file(s)")

            selectedOption = selectOptions([
                                            "search for interesting stuff in online",
                                            "download the js files in local then search for interresting stuff at local",
                                            "exit"
                                            ])
            
            if selectedOption == "search for interesting stuff in online":
                with yaspin(text=f"", color="yellow") as sp:
                    searchStuffOnline(js_files, sp)
                
            else:
                with yaspin(text=f"", color="yellow") as sp:
                    sp.write(f"\n<------------- {yellow}Downloading Logs{reset} ------------->")
                    jsFolder_path = downloadJsFiles(js_files=js_files, sp=sp)

                    sp.write(f"\n<------------------- {yellow}Logs{reset} ------------------->")
                    searchStuffInLocal(jsFolder_path, sp=sp)

        else:
            print("Nothing found :(\nQuitting...")
            exit()
    else:
        print(f"\n<------------- {yellow}Enter the Path{reset} --------------->")
        print(f"{yellow}[+]{reset} please enter js files directory:")
        jsFolder_path = input(f"{yellow}>> {reset}")

        for _ in range(3):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        sys.stdout.flush()
        with yaspin(text=f"", color="yellow") as sp:
            sp.write(f"<------------------- {yellow}Logs{reset} ------------------->")
            searchStuffInLocal(folder_path=jsFolder_path, sp=sp)

        
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
