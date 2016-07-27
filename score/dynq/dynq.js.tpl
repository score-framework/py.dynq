// Copyright © 2015 STRG.AT GmbH, Vienna, Austria
//
// This file is part of the The SCORE Framework.
//
// The SCORE Framework and all its parts are free software: you can redistribute
// them and/or modify them under the terms of the GNU Lesser General Public
// License version 3 as published by the Free Software Foundation which is in the
// file named COPYING.LESSER.txt.
//
// The SCORE Framework and all its parts are distributed without any WARRANTY;
// without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
// PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
// License.
//
// If you have not received a copy of the GNU Lesser General Public License see
// http://www.gnu.org/licenses/.
//
// The License-Agreement realised between you as Licensee and STRG.AT GmbH as
// Licenser including the issue of its valid conclusion and its pre- and
// post-contractual effects is governed by the laws of Austria. Any disputes
// concerning this License-Agreement including the issue of its valid conclusion
// and its pre- and post-contractual effects are exclusively decided by the
// competent court, in whose district STRG.AT GmbH has its registered seat, at
// the discretion of STRG.AT GmbH also the competent court, in whose district the
// Licensee has his registered seat, an establishment or assets.

define('%s', ['%s', 'score.init', 'score.oop', 'score.dynq'], function(Api, score) {

    var api = new Api();

    score.extend('dynq.py', ['oop'], function() {

        var DataSource = score.oop.Class({
            __name__: 'PythonDataSource',
            __parent__: score.dynq.PollingDataSource,

            _poll: function(self, queries) {
                var data = [];
                for (var i = 0; i < queries.length; i++) {
                    var query = queries[i];
                    data.push([query.query, query.mtime, query.autoupdate]);
                }
                return api.handle_queries(self.name, data);
            }

        });

        var sources = [%s];

        for (var i = 0; i < sources.length; i++) {
            score.dynq.register(new DataSource(sources[i]));
        }

        return {

            DataSource: DataSource

        };

    });

});
