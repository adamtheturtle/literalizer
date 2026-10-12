(create-ns 'obj)
(intern 'obj 'BEGIN (fn [& _args] nil))
(obj/BEGIN :a 42)
