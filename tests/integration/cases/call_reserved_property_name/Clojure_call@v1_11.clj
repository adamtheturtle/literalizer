(create-ns 'foo)
(intern 'foo 'class (fn [& _args] nil))
(foo/class :value 1)
