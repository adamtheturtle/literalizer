(create-ns 'app.client)
(intern 'app.client 'fetch (fn [& _args] nil))
(app.client/fetch :value "hello")
(app.client/fetch :value "world")
