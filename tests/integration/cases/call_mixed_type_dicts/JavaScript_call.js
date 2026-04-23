var mgr = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
mgr.Op({ operation: {"type": "create", "pr_id": "pr_1", "draft": true} });
mgr.Op({ operation: {"type": "create", "pr_id": "pr_2"} });
