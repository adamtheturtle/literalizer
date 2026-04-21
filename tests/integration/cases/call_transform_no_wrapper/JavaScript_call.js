var client = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
client.api.request({ data: "hello" });
client.api.request({ data: 42 });
client.api.request({ data: true });
