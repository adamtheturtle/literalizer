var app = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
function emit() {}
emit(app.client.fetch({ payload: "hello" }));
emit(app.client.fetch({ payload: 42 }));
emit(app.client.fetch({ payload: true }));
