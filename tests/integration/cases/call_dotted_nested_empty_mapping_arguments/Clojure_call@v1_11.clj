(create-ns 'api.worker)
(intern 'api.worker 'process (fn [& _args] nil))
(api.worker/process :values [1 {}] :count 42)
(api.worker/process :values [2 {"x" "s"}] :count 43)
