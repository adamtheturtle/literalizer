fn main() {
    let event_index = std::cell::Cell::new(0_usize);
    let observe_event = |actual: i32| {
        let expected = [2, 0, 1, 1, 2, 101];
        let index = event_index.get();
        assert!(index < 6);
        assert_eq!(actual, expected[index]);
        event_index.set(index + 1);
    };
    let make_widget = |count: i32| { observe_event(1); observe_event(count); count + 100 };
    let consume_widget = |count: i32| { observe_event(2); observe_event(count); };
    let verify_events = || { assert_eq!(event_index.get(), 6); };
    let mut my_data = 0;
    consume_widget(my_data);
    my_data = make_widget(1);
    consume_widget(my_data);
    verify_events();
}
