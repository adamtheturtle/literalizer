@discardableResult func make_widget(count: Any = 0) -> Any { 0 }
@discardableResult func consume_widget(count: Any = 0) -> Any { 0 }
var my_data = make_widget(count: 42)
consume_widget(count: my_data);
my_data = make_widget(count: 42) // note
consume_widget(count: my_data);
