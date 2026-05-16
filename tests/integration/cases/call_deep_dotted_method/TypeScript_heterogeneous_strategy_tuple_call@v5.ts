const obj: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
obj.api.client.post({ data: "hello" });
obj.api.client.post({ data: 42 });
obj.api.client.post({ data: true });
export {};
