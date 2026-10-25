const obj: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
const my_data = obj.ZVal({ _arg: 42 }) // note;
export {};
