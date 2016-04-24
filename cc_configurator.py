# File: cc_configurator.py
# Description:  This file provides an interface to program options. It's really basic.
#				It just loads and saves a JSON file and provides a name to access it by

import json

config = {'auto-connect':True
			}

def get_cc_config():
	return config
