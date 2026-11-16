fn main() {
    let event_index = std::cell::Cell::new(0_usize);
    let observe_event = |actual: i32| {
        let expected = [1, 42, 2, 142];
        let index = event_index.get();
        assert!(index < 4);
        assert_eq!(actual, expected[index]);
        event_index.set(index + 1);
    };
    let make_widget = |value: i32| { observe_event(1); observe_event(value); value + 100 };
    let consume = |value: i32| { observe_event(2); observe_event(value); };
    let verify_events = || { assert_eq!(event_index.get(), 4); };
    let my_data = make_widget(42);
    consume(my_data.clone());
    verify_events();
}
