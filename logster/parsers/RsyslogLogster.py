###  A logster parser file that can be used to keep track of queue size outputed by rsyslogd-pstats module
###
###  For example:
###  sudo ./logster --dry-run --output=ganglia RsyslogLog /var/log/messages
###
###

import time
import re

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class RsyslogLogster(LogsterParser):

    def __init__(self, option_string=None):
        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''
        self.values = dict(size=None, enqueued=None, full=None, maxqsize=None)

        # Regular expression for matching lines we are interested in, and capturing
        # fields from the line
        #self.reg = re.compile('^\[[^]]+\] \[(?P<loglevel>\w+)\] .*')
        self.reg = re.compile('.*rsyslogd-pstats: main Q: size=(\d+) enqueued=(\d+) full=(\d+) discarded.full=(\d+) discarded.nf=(\d+) maxqsize=(\d+)')


    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''

        try:
            # Apply regular expression to each line and extract interesting bits.
            regMatch = self.reg.match(line)

            if regMatch:
                match = regMatch.groups()
                self.values['size'] = match[0]
                self.values['enqueued'] = match[1]
                self.values['full'] = match[2]
                self.values['discarded.nf'] = match[3]
                self.values['maxqsize'] = match[4]
            else:
                raise "No match"

        except Exception, e:
            raise LogsterParsingException, "regmatch or contents failed with %s" % e


    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''

        # Return a list of metrics objects

        return [ MetricObject(name, value, "None") for (name,value) in self.values.items() if value > 0]
