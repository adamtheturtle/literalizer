@discardableResult func f(ops: Any = 0) -> Any { 0 }
f(ops: [["DEL", "b", "10"], ["ADD", "a", "x"]]);  // note
// next call
f(ops: [["ADD", "c", "y"]]);
