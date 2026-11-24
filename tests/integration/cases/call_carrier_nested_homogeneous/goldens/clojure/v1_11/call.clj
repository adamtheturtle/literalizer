(create-ns 'app.client)
(intern 'app.client 'go (fn [& _args] nil))
(app.client/go :first_value [1] :second_value [2])
