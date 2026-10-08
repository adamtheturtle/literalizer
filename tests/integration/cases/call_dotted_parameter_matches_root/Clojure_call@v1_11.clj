(create-ns 'outer)
(intern 'outer 'inner (fn [& _args] nil))
(outer/inner :outer 1 :n 2)
