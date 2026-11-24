@discardableResult func make_widget(value: Any = 0) -> Any { 0 }
@discardableResult func consume(value: Any = 0) -> Any { 0 }
var my_data = make_widget(value: 42)
consume(value: my_data);
my_data = make_widget(value: 42)
consume(value: my_data);
