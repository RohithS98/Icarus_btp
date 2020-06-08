"""This module contains all configuration information used to run simulations
"""
from multiprocessing import cpu_count
from collections import deque
import copy
from icarus.util import Tree

# GENERAL SETTINGS

# Level of logging output
# Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# If True, executes simulations in parallel using multiple processes
# to take advantage of multicore CPUs
PARALLEL_EXECUTION = True

# Number of processes used to run simulations in parallel.
# This option is ignored if PARALLEL_EXECUTION = False
N_PROCESSES = cpu_count()

# Granularity of caching.
# Currently, only OBJECT is supported
CACHING_GRANULARITY = 'OBJECT'

# Format in which results are saved.
# Result readers and writers are located in module ./icarus/results/readwrite.py
# Currently only PICKLE is supported 
RESULTS_FORMAT = 'PICKLE'

# Number of times each experiment is replicated
# This is necessary for extracting confidence interval of selected metrics
N_REPLICATIONS = 10

# List of metrics to be measured in the experiments
# The implementation of data collectors are located in ./icaurs/execution/collectors.py
#DATA_COLLECTORS = ['CACHE_HIT_RATIO', 'PATH_STRETCH', 'EVICTIONS']
DATA_COLLECTORS = ['CACHE_HIT_RATIO', 'UTILIZATION', 'EVICTIONS', 'DIVERSITY', 'PATH_STRETCH']

# Range of alpha values of the Zipf distribution using to generate content requests
# alpha values must be positive. The greater the value the more skewed is the 
# content popularity distribution
# Range of alpha values of the Zipf distribution using to generate content requests
# alpha values must be positive. The greater the value the more skewed is the 
# content popularity distribution
# Note: to generate these alpha values, numpy.arange could also be used, but it
# is not recommended because generated numbers may be not those desired. 
# E.g. arange may return 0.799999999999 instead of 0.8. 
# This would give problems while trying to plot the results because if for
# example I wanted to filter experiment with alpha=0.8, experiments with
# alpha = 0.799999999999 would not be recognized 
ALPHA = [0.4, 0.7, 1, 1.3, 1.6]

# Total size of network cache as a fraction of content population
NETWORK_CACHE = [0.04]

# Number of content objects
N_CONTENTS = 7*10**3

# Number of requests per second (over the whole network)
NETWORK_REQUEST_RATE = 10.0

# Number of content requests generated to prepopulate the caches
# These requests are not logged
N_WARMUP_REQUESTS = 3*10**3

# Number of content requests generated after the warmup and logged
# to generate results. 
N_MEASURED_REQUESTS = 2*10**5

# List of all implemented topologies
# Topology implementations are located in ./icarus/scenarios/topology.py
TOPOLOGIES =  [
        'TEST_TOP',
        #'GEANT_2',
              ]

# List of caching and routing strategies
# The code is located in ./icarus/models/strategy.py
STRATEGIES = [
     'LCD',             
     #'PROB_CACHE',      # ProbCache
     'LCD',             # Leave Copy Down
     'LCD',
     'TEST',
     'TEST',
     'TEST',
     'LCE',
     'LCE',
     'LCE',
     'PROB_CACHE',
     'PROB_CACHE',
     'PROB_CACHE',
             ]

# Cache replacement policy used by the network caches.
# Supported policies are: 'LRU', 'LFU', 'FIFO', 'RAND' and 'NULL'
# Cache policy implmentations are located in ./icarus/models/cache.py
CACHE_POLICIES = ['BIP','EAF','LRU']*4

# Queue of experiments
EXPERIMENT_QUEUE = deque()
default = Tree()
default['workload'] = {'name':       'STATIONARY',
                       'n_contents': N_CONTENTS,
                       'n_warmup':   N_WARMUP_REQUESTS,
                       'n_measured': N_MEASURED_REQUESTS,
                       'rate':       NETWORK_REQUEST_RATE
                       }
default['cache_placement']['name'] = 'UNIFORM'
default['content_placement']['name'] = 'UNIFORM'
#default['cache_policy']['name'] = CACHE_POLICY

# Create experiments multiplexing all desired parameters
for alpha in ALPHA:
    for strategy, cache_policy in zip(STRATEGIES,CACHE_POLICIES):
        for topology in TOPOLOGIES:
            for network_cache in NETWORK_CACHE:
                experiment = copy.deepcopy(default)
                experiment['workload']['alpha'] = alpha
                experiment['strategy']['name'] = strategy
                experiment['cache_policy']['name'] = cache_policy
                experiment['topology']['name'] = topology
                experiment['cache_placement']['network_cache'] = network_cache
                experiment['desc'] = "Alpha: %s, strategy: %s, topology: %s, cache policy: %s, network cache: %s" \
                 % (str(alpha), strategy, topology, str(cache_policy), str(network_cache))
                EXPERIMENT_QUEUE.append(experiment)
