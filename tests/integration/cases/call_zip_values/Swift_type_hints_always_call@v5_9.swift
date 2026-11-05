@discardableResult func process(value: Any = 0) -> Any { 0 }
@discardableResult func emit(_call: Any = 0, _zip: Any = 0) -> Any { 0 }
emit(_call: process(value: "hello"), _zip: true);
emit(_call: process(value: 42), _zip: false);
