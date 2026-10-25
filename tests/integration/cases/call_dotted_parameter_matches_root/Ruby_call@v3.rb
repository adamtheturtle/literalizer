class OuterType; def inner(*a, **kw); end; end
outer = OuterType.new
outer.inner(outer: 1, n: 2)
