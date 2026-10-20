const thing: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
const item = [
  1,
  2,
];
thing.go({ value: item });
export {};
