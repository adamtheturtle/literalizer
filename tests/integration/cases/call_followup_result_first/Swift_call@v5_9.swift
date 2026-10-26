@discardableResult func make_widget(first: Any = 0, second: Any = 0) -> Any { 0 }
@discardableResult func consume(first: Any = 0, second: Any = 0) -> Any { 0 }
let my_data = make_widget(first: 42, second: 3)
consume(first: my_data, second: 3);
