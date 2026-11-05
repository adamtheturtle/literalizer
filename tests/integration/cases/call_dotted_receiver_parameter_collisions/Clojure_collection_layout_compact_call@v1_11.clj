(create-ns 'api.worker)
(intern 'api.worker 'process (fn [& _args] nil))
(api.worker/process :self {} :self_ {})
