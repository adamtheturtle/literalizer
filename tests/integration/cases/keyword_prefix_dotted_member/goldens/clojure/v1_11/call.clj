(create-ns 'thing)
(intern 'thing 'first_value (fn [& _args] nil))
(thing/first_value :value 1)
