const app: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
const emit: any = () => {};
emit(app.client.fetch({ payload: "hello" }));
emit(app.client.fetch({ payload: 42 }));
emit(app.client.fetch({ payload: true }));
export {};
