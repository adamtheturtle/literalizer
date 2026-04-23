(defn mgr [& _args] nil)
(defn mgr.Op [& _args] nil)
(mgr.Op :operation {"type" "create" "pr_id" "pr_1" "draft" true})
(mgr.Op :operation {"type" "create" "pr_id" "pr_2"})
