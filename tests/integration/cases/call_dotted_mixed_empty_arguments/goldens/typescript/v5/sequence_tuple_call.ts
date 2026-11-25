const thing: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
thing.go({ before: [] as const, populated: [1] as const, after: [] as const });
thing.go({ before: ["text"] as const, populated: [2] as const, after: [] as const });
thing.go({ before: [] as const, populated: ["text"] as const, after: [] as const });
thing.go({ before: ["text"] as const, populated: [2] as const, after: [3] as const });
export {};
