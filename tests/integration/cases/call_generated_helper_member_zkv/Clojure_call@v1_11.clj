(create-ns 'obj)
(intern 'obj 'ZKV (fn [& _args] nil))
(obj/ZKV :value 1)
