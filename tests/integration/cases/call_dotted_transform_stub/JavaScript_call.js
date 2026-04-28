function process() {}
var log = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
log.emit(process({ value: "hello" }));
log.emit(process({ value: 42 }));
log.emit(process({ value: true }));
