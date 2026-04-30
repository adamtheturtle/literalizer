local app = { mgr: { run(operation):: null } };
[
    app.mgr.run(operation={type: "create", pr_id: "pr_1", draft: true}),
    app.mgr.run(operation={type: "create", pr_id: "pr_2"}),
]
