(defn process [& _args] nil)
(def my_var 42)
(process :data {"key" {"ref" "my_var"} "count" 42})
