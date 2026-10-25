@discardableResult func f(a: Any = 0) -> Any { 0 }
@discardableResult func repr(_arg: Any = 0) -> Any { 0 }
let ref_data = 1
repr(_arg: f(a: ref_data));
