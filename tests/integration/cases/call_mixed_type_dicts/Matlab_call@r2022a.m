app.mgr.run = @(varargin) [];
app.mgr.run(struct('type', "create", 'pr_id', "pr_1", 'draft', true))
app.mgr.run(struct('type', "create", 'pr_id', "pr_2"))
