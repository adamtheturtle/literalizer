const process: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
process.api.fetch({ data: {"data": "hello"} });
process.api.fetch({ data: {"data": 42} });
process.api.fetch({ data: {"data": true} });
export {};
