var app = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
app.mgr.run({ operation: {"type": "create", "pr_id": "pr_1", "draft": true} });
app.mgr.run({ operation: {"type": "create", "pr_id": "pr_2"} });
