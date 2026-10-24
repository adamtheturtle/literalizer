(create-ns 'class)
(intern 'class 'member (fn [& _args] nil))
(class/member :a 42)
