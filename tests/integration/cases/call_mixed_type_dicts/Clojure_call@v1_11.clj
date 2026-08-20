(create-ns 'app.mgr)
(intern 'app.mgr 'run (fn [& _args] nil))
(app.mgr/run :operation {"type" "create" "pr_id" "pr_1" "draft" true})
(app.mgr/run :operation {"type" "create" "pr_id" "pr_2"})
