const thing: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
const my_data = thing.go({ value: [] });
export {};
