import sys
import itertools
from automation import TaskManager, CommandSequence

# Number of sites to crawl
site_limit = int(sys.argv[1])
sites_file = './sites.txt'

def iterate_sites():
    with open(sites_file) as fp:
        for line in fp:
            yield line.strip()

NUM_BROWSERS = 2
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in xrange(NUM_BROWSERS):
    browser_params[i]['http_instrument'] = True # Record HTTP Requests and Responses
    browser_params[i]['disable_flash'] = False #Enable flash for all three browsers
    browser_params[i]['screen_res'] = '800x500'
# second browser has no third party cookies
browser_params[1]['tp_cookies'] = 'never'

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/'
manager_params['log_directory'] = '~/'

# Instantiates the measurement platform
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for site in itertools.islice(iterate_sites(), site_limit):
    command_sequence = CommandSequence.CommandSequence(site)

    # Start by visiting the page
    command_sequence.browse(1, sleep=0, timeout=60)

    manager.execute_command_sequence(command_sequence, index='*') # ** = synchronized browsers

# Shuts down the browsers and waits for the data to finish logging
manager.close()
