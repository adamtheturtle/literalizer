var app = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
app.mgr.op({ operation: {"type": "create", "pr_id": "pr_1", "draft": true} });
app.mgr.op({ operation: {"type": "create", "pr_id": "pr_2"} });
