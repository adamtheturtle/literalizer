(create-ns 'helper)
(intern 'helper 'list (fn [& _args] nil))
(helper/list :a 1)
