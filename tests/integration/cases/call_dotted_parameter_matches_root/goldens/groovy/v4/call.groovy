class _OuterType { def inner(Map _args) { null } }
def outer = new _OuterType()
outer.inner(outer: 1, n: 2)
