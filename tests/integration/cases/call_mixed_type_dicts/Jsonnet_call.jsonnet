local app = { mgr: { op(operation):: null } };
[
    app.mgr.op(operation={type: "create", pr_id: "pr_1", draft: true}),
    app.mgr.op(operation={type: "create", pr_id: "pr_2"}),
]
