var thing = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
thing.go({ before: [], populated: [1], after: [] });
thing.go({ before: ["text"], populated: [2], after: [] });
thing.go({ before: [], populated: ["text"], after: [] });
thing.go({ before: ["text"], populated: [2], after: [3] });
