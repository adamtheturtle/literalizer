(create-ns 'a.foo.Foo)
(intern 'a.foo.Foo 'bar (fn [& _args] nil))
(a.foo.Foo/bar :x [1])
