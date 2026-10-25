class _outerType { @discardableResult func inner(outer: Any = 0, n: Any = 0) -> Any { 0 } }
let outer = _outerType()
outer.inner(outer: 1, n: 2);
