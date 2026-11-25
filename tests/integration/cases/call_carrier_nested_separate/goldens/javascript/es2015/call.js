var app = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
app.client.go({ first_value: [1], second_value: ["text"] });
