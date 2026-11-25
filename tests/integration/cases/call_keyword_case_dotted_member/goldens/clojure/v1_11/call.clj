(create-ns 'thing)
(intern 'thing 'Before (fn [& _args] nil))
(thing/Before :value 1)
