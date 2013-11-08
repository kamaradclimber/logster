###  A logster parser file that can be used to keep track of the number of log lines per host.
###
###  For example:
###  sudo ./logster --dry-run --output=ganglia LogByHost /var/log/a_log.log
###
###

import time
import re

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class LogByHostLogster(LogsterParser):

    def __init__(self, option_string=None):
        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''
        self.values = dict()

        # Regular expression for matching lines we are interested in, and capturing
        # fields from the line
        self.reg = re.compile('^[^\s]+ ([^\s]+)')


    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''

        try:
            # Apply regular expression to each line and extract interesting bits.
            regMatch = self.reg.findall(line)

            if regMatch:
                host = re.sub(r'\.', '_', regMatch[0])
                self.values[host] = self.values.get(host, 0) + 1
            else:
                raise "No match"

        except Exception, e:
            raise LogsterParsingException, "regmatch or contents failed with %s" % e


    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''

        # Return a list of metrics objects

        return [ MetricObject(name, value, "None") for (name,value) in self.values.items() if value > 0]
