(create-ns 'foo.Foo)
(intern 'foo.Foo 'bar (fn [& _args] nil))
(foo.Foo/bar :x [1])
