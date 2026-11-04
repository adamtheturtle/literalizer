class _thingType { @discardableResult func go(before: Any = 0, populated: Any = 0, after: Any = 0) -> Any { 0 } }
let thing = _thingType()
thing.go(before: [Any](), populated: [1], after: [Any]());
thing.go(before: ["text"], populated: [2], after: [Any]());
thing.go(before: [Any](), populated: ["text"], after: [Any]());
thing.go(before: ["text"], populated: [2], after: [3]);
