(create-ns 'app)
(intern 'app 'go (fn [& _args] nil))
(app/go :first_value [1] :second_value [2])
