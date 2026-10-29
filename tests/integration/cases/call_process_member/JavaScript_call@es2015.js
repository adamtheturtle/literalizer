var app = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
app.process.fetch({ data: {"data": "hello"} });
app.process.fetch({ data: {"data": 42} });
app.process.fetch({ data: {"data": true} });
