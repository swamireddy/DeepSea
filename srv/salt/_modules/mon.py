#!/usr/bin/python

import rados
import json
import time
import logging
import pprint

log = logging.getLogger(__name__)

"""
The need for this module is that the roles show the intended state and not
the current state.  Once the admin unassigns the monitor role, the pillar reflects that configuration.
"""


class Monitors(object):
    """
    Connect to ceph to determine the monitors
    """

    def __init__(self, **kwargs):
        """
        Default settings can be overridden
        """

        self.settings = {
            'conf' : "/etc/ceph/ceph.conf",
            'timeout': 300,
            'check': 2,
            'delay': 6,
            'negate': False
        }
        self.settings.update(kwargs)
        log.debug("settings: {}".format(_skip_dunder(self.settings)))
        self._connect()

    def _connect(self):
        """
        Connect to Ceph cluster
        """
        self.cluster=rados.Rados(conffile=self.settings['conf'])
        self.cluster.connect()

    def list(self):
        """
        Returns the keys
        """
        return [ entry['name'] for entry in self._dump() ]

    def _dump(self):
        """
        Call ceph mon dump
        """
        cmd = json.dumps({"prefix":"mon dump", "format":"json" })
        ret,output,err = self.cluster.mon_command(cmd, b'', timeout=6)
        dump = json.loads(output)['mons']
        log.debug("status: {}".format(dump))
        return dump



def list(**kwargs):
    """
    List the monitors
    """
    m = Monitors(**kwargs)
    return m.list()



def _skip_dunder(settings):
    """
    Skip double underscore keys
    """
    return {k:v for k,v in settings.iteritems() if not k.startswith('__')}

