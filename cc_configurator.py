# File: cc_configurator.py
# Description:  This file provides an interface to program options.
#				This stores the default program configuration, if one cannot
#				be loaded from disk.
# Included in the configuration:
# - Program interface preferences
# - Configured services. These are CatChat servers

import json
import os.path

default_config = {	'auto-connect':True,
					'services':[
						{
						'display-name'	:'Main Server',
						'server-type'	:'url',
						'server-url'	:'http://107.150.59.253/',
						'username'		:'james',
						'password'		:'computer'
						}
						]
				}

config = None

def get_cc_config():
	global config
	if config is None:
		if not os.path.isfile("~/.catchat"):
			print "No configuration file. Using defaults"
			config = default_config

	return config
