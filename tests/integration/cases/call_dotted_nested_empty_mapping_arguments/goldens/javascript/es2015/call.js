var api = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
api.worker.process({ values: [1, {}], count: 42 });
api.worker.process({ values: [2, {"x": "s"}], count: 43 });
