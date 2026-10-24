(create-ns 'obj)
(intern 'obj 'ZVal (fn [& _args] nil))
(obj/ZVal :value 1)
