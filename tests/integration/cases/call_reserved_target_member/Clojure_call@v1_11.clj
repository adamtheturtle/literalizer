(create-ns 'obj)
(intern 'obj 'class (fn [& _args] nil))
(obj/class :a 42)
