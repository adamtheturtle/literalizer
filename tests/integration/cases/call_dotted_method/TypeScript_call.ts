const app: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
app.client.fetch({ payload: "hello" });
app.client.fetch({ payload: 42 });
app.client.fetch({ payload: true });
export {};
