@discardableResult func make_widget(before: Any = 0, populated: Any = 0, after: Any = 0) -> Any { 0 }
make_widget(before: (), populated: (1), after: ());
make_widget(before: ("text"), populated: (2), after: ());
make_widget(before: (), populated: ("text"), after: ());
make_widget(before: ("text"), populated: (2), after: (3));
