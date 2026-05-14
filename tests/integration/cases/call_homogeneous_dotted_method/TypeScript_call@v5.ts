const app: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
app.client.fetch({ value: "hello" });
app.client.fetch({ value: "world" });
export {};
