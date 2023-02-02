import utils.scrap as scrap
import argparse


print(open('misc/ascii2.txt', 'r').read())
parser = argparse.ArgumentParser(description="Terminal application for ripping API around internet and searching REALLY valid PROXIES")

# Proxy Attempts argument settings
parser.add_argument("--attempts","-a", 
    help="Retries for proxy connection, until it considered failed (default : 4)",
    default=4,
    type=int)

# Proxy Time for timeout argument settings
parser.add_argument("--timeout", 
    help="Time defined when in specific time getting no response using proxy (default : 2)",
    default=2,
    type=int)

# Option argument for disabling thread count
parser.add_argument("--disable-cache", 
    help="Option for disabling default proxy caching for latest session (default : cache enabled)",
    action='store_true')

# No argument option for disabling proxy caching
parser.add_argument("--threads", '-t', 
    help="Count of threads used for proxy validation (default : 10)",
    default=10,
    type=int)

# No argument option for disabling proxy caching
parser.add_argument("--check-url", "-u", 
    help="URL API for testing response to determine proxy validity (default : https://www.myip.com)",
    default="https://www.myip.com",
    type=str)

# No argument option for disabling proxy caching
parser.add_argument('--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()


scrap.runScraping(args)