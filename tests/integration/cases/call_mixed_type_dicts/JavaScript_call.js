var m = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
m.Op({ operation: {"type": "create", "pr_id": "pr_1", "draft": true} });
m.Op({ operation: {"type": "create", "pr_id": "pr_2"} });
