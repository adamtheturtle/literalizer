(create-ns 'a.foo.Foo)
(intern 'a.foo.Foo 'bar (fn [& _args] 0))
(def my_data (a.foo.Foo/bar :x [1]))
