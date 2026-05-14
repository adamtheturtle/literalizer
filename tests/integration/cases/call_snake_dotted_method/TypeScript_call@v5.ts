const my_app: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
my_app.http_client.fetch({ payload: "hello" });
my_app.http_client.fetch({ payload: 42 });
my_app.http_client.fetch({ payload: true });
export {};
