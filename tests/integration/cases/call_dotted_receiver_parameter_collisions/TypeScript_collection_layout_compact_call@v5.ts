const api: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
api.worker.process({ self: {}, self_: {} });
export {};
