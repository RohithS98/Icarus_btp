#!/usr/bin/env python
"""Plot results read from a result set
"""
from __future__ import division
import os
import argparse
import collections
import logging

import numpy as np
import matplotlib.pyplot as plt

from icarus.util import Settings, Tree, config_logging, step_cdf
from icarus.tools import means_confidence_interval
from icarus.results import plot_lines, plot_bar_chart
from icarus.registry import RESULTS_READER


# Logger object
logger = logging.getLogger('plot')

# These lines prevent insertion of Type 3 fonts in figures
# Publishers don't want them
plt.rcParams['ps.useafm'] = True
plt.rcParams['pdf.use14corefonts'] = True

# If True text is interpreted as LaTeX, e.g. underscore are interpreted as 
# subscript. If False, text is interpreted literally
plt.rcParams['text.usetex'] = False

# Aspect ratio of the output figures
plt.rcParams['figure.figsize'] = 8, 5

# Size of font in legends
LEGEND_SIZE = 14

# Line width in pixels
LINE_WIDTH = 1.5

# Plot
PLOT_EMPTY_GRAPHS = True

# This dict maps strategy names to the style of the line to be used in the plots
# Off-path strategies: solid lines
# On-path strategies: dashed lines
# No-cache: dotted line
CACHE_STYLE = {
         'LRU':             'b--p',
         'BIP':             'g-->',
         'PROB_CACHE':      'c--<',
         'TEST':  	    'r--*',
                }

# This dict maps name of strategies to names to be displayed in the legend
CACHE_LEGEND = {
         'LRU':             'LRU',
         'BIP':             'BIP',
         'PROB_CACHE':      'ProbCache',
         'TEST':	    'Test Cache',
                    }

# Color and hatch styles for bar charts of cache hit ratio and link load vs topology
CACHE_BAR_COLOR = {
    'LRU':          'k',
    'BIP':          '0.4',
    }

CACHE_BAR_HATCH = {
    'LRU':          None,
    'BIP':          '//',
    }

def plot_general_policy(resultset, policies, strategies, cache_size, alpha, plotdir, title, ylab, ymetric, name):
	print(policies, strategies, cache_size, alpha)
	desc = {}
	desc['title'] = title
	desc['ylabel'] = ylab
	desc['xparam'] = ('strategy', 'name')
	desc['xvals'] = list(set(strategies))
	desc['filter'] = {'cache_placement': {'network_cache': cache_size},
                      'workload': {'name': 'STATIONARY', 'alpha': alpha}}
	desc['ymetrics'] = [ymetric]*len(list(set(strategies)))
	desc['ycondnames'] = [('cache_policy', 'name')]*len(list(set(strategies)))
	desc['ycondvals'] = list(set(policies))
	desc['errorbar'] = True
	desc['legend_loc'] = 'lower right'
	desc['bar_color'] = CACHE_BAR_COLOR
	desc['bar_hatch'] = CACHE_BAR_HATCH
	desc['legend'] = CACHE_LEGEND
	desc['plotempty'] = PLOT_EMPTY_GRAPHS
	
	plot_bar_chart(resultset, desc, name, plotdir)

def plot_cache_hit(resultset, policies, strategies, cache_size, alpha, plotdir):
	plot_general_policy(resultset, policies, strategies, cache_size, alpha, plotdir, 'Cache Hit Ratio vs Policy', 'Cache Hit Ratio', ('CACHE_HIT_RATIO', 'MEAN'), 'Cache_Hit_Ratio_Policy.png')
	
def plot_path_stretch(resultset, policies, strategies, cache_size, alpha, plotdir):
	plot_general_policy(resultset, policies, strategies, cache_size, alpha, plotdir, 'Path Stretch vs Strategy', 'Path Stretch', ('PATH_STRETCH', 'MEAN'), 'Path_Stretch_Policy.png')
	
def plot_cache_evictions(resultset, policies, strategies, cache_size, alpha, plotdir):
	plot_general_policy(resultset, policies, strategies, cache_size, alpha, plotdir, 'Cache Evictions vs Policy', 'Cache Evictions', ('EVICTIONS', 'NUMBER'), 'Cache_Evictions_Policy.png')
	
def plot_cache_utilization(resultset, policies, strategies, cache_size, alpha, plotdir):
	plot_general_policy(resultset, policies, strategies, cache_size, alpha, plotdir, 'Cache Utilization vs Policy', 'Cache Utilization', ('UTILIZATION', 'MEAN'), 'Cache_Utilization_Policy.png')
	
def plot_cache_diversity(resultset, policies, strategies, cache_size, alpha, plotdir):
	plot_general_policy(resultset, policies, strategies, cache_size, alpha, plotdir, 'Cache Diversity vs Policy', 'Cache Diversity', ('DIVERSITY', 'MEAN'), 'Cache_Diversity_Strategy.png')

def run(config, results, plotdir):
    """Run the plot script
    
    Parameters
    ----------
    config : str
        The path of the configuration file
    results : str
        The file storing the experiment results
    plotdir : str
        The directory into which graphs will be saved
    """
    settings = Settings()
    settings.read_from(config)
    config_logging(settings.LOG_LEVEL)
    resultset = RESULTS_READER[settings.RESULTS_FORMAT](results)
    #print(resultset.prettyprint())
    # Create dir if not existsing
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
    # Parse params from settings
    topologies = settings.TOPOLOGIES
    cache_sizes = settings.NETWORK_CACHE
    alphas = settings.ALPHA
    strategies = settings.STRATEGIES
    policies = settings.CACHE_POLICIES
    # Plot graphs
    
    plot_cache_hit(resultset, policies, strategies, cache_sizes[0], alphas[0], plotdir)
    plot_path_stretch(resultset, policies, strategies, cache_sizes[0], alphas[0], plotdir)
    plot_cache_evictions(resultset, policies, strategies, cache_sizes[0], alphas[0], plotdir)
    plot_cache_utilization(resultset, policies, strategies, cache_sizes[0], alphas[0], plotdir)
    plot_cache_diversity(resultset, policies, strategies, cache_sizes[0], alphas[0], plotdir)
    
    '''
    for cache_size in cache_sizes:
        for alpha in alphas:
            logger.info('Plotting cache hit ratio for cache size %s vs alpha %s against topologies' % (str(cache_size), str(alpha)))
            plot_cache_hits_vs_topology(resultset, alpha, cache_size, topologies, strategies, plotdir)
    logger.info('Exit. Plots were saved in directory %s' % os.path.abspath(plotdir))
'''

def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("-r", "--results", dest="results",
                        help='the results file',
                        required=True)
    parser.add_argument("-o", "--output", dest="output",
                        help='the output directory where plots will be saved',
                        required=True)
    parser.add_argument("config",
                        help="the configuration file")
    args = parser.parse_args()
    run(args.config, args.results, args.output)

if __name__ == '__main__':
    main()



'''def plot_cache_hit(resultset, policies, strategies, cache_size, alpha, plotdir):
	print(policies, strategies, cache_size, alpha)
	desc = {}
	desc['title'] = 'Cache Hit Ratio vs Policy'
	desc['ylabel'] = 'Cache Hit Ratio'
	desc['xparam'] = ('strategy', 'name')
	desc['xvals'] = list(set(strategies))
	desc['filter'] = {'cache_placement': {'network_cache': cache_size},
                      'workload': {'name': 'STATIONARY', 'alpha': alpha}}
	desc['ymetrics'] = [('CACHE_HIT_RATIO', 'MEAN')]*len(list(set(strategies)))
	desc['ycondnames'] = [('cache_policy', 'name')]*len(list(set(strategies)))
	desc['ycondvals'] = list(set(policies))
	desc['errorbar'] = True
	desc['legend_loc'] = 'lower right'
	desc['bar_color'] = CACHE_BAR_COLOR
	desc['bar_hatch'] = CACHE_BAR_HATCH
	desc['legend'] = CACHE_LEGEND
	desc['plotempty'] = PLOT_EMPTY_GRAPHS
	
	plot_bar_chart(resultset, desc, 'Cache_Hit_Ratio_Policy.png', plotdir)'''
