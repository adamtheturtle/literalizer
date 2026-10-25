(create-ns 'api)
(intern 'api 'process (fn [& _args] nil))
(api/process :self {})
