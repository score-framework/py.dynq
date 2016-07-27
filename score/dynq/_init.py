# Copyright © 2016 STRG.AT GmbH, Vienna, Austria
#
# This file is part of the The SCORE Framework.
#
# The SCORE Framework and all its parts are free software: you can redistribute
# them and/or modify them under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation which is in the
# file named COPYING.LESSER.txt.
#
# The SCORE Framework and all its parts are distributed without any WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
# License.
#
# If you have not received a copy of the GNU Lesser General Public License see
# http://www.gnu.org/licenses/.
#
# The License-Agreement realised between you as Licensee and STRG.AT GmbH as
# Licenser including the issue of its valid conclusion and its pre- and
# post-contractual effects is governed by the laws of Austria. Any disputes
# concerning this License-Agreement including the issue of its valid conclusion
# and its pre- and post-contractual effects are exclusively decided by the
# competent court, in whose district STRG.AT GmbH has its registered seat, at
# the discretion of STRG.AT GmbH also the competent court, in whose district the
# Licensee has his registered seat, an establishment or assets.

import json
import os
from score.init import ConfiguredModule, parse_dotted_path, parse_list
from score.jsapi import UrlEndpoint


defaults = {
    'sources': [],
    'jsapi.name': 'dynq',
    'jslib.require': 'score.dynq.py',
}


def init(confdict, jsapi):
    """
    Initializes this module according to :ref:`our module initialization
    guidelines <module_initialization>` with the following configuration keys:

    """
    conf = dict(defaults.items())
    conf.update(confdict)
    sources = list(map(parse_dotted_path, parse_list(conf['sources'])))
    dynq = ConfiguredDynqModule(jsapi, sources, conf['jsapi.name'])

    if jsapi.jslib:
        import score.dynq

        @jsapi.jslib.virtlib(conf['jslib.require'], score.dynq.__version__,
                             ['score.init', 'score.oop', 'score.dynq'])
        def api(ctx):
            return dynq.generate_js()

    return dynq


def _genjs(require_name, jsapi_name, sources):
    return js_tpl % (require_name, jsapi_name,
                     json.dumps(list(sources.keys())))


class ConfiguredDynqModule(ConfiguredModule, UrlEndpoint):

    def __init__(self, jsapi, sources, name):
        import score.dynq
        ConfiguredModule.__init__(self, score.dynq)
        UrlEndpoint.__init__(self, name)
        self.sources = dict((s.name, s) for s in sources)
        self.jsapi = jsapi
        self.op(self.handle_queries)
        self.jsapi.add_endpoint(self)

    def handle_queries(self, ctx, name, queries):
        return list(self.sources[name].handle_queries(ctx, queries))

    def generate_js(self):
        if not hasattr(self, '__generated_js'):
            self.__generated_js = _genjs(
                self.require_name, self.jsapi.require_name, self.sources)
        return self.__generated_js


here = os.path.abspath(os.path.dirname(__file__))
file = os.path.join(here, 'dynq.js.tpl')
js_tpl = open(file).read()
