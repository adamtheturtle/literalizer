const app: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
app.go({ first_value: [1], second_value: ["text"] });
export {};
