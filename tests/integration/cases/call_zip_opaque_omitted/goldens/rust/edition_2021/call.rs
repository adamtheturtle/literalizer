fn main() {
    let event_index = std::cell::Cell::new(0_usize);
    let observe_event = |actual: i32| {
        let expected = [1, 1];
        let index = event_index.get();
        assert!(index < 2);
        assert_eq!(actual, expected[index]);
        event_index.set(index + 1);
    };
    let process = |value: i32| { observe_event(1); observe_event(value); value + 100 };
    let verify_events = || { assert_eq!(event_index.get(), 2); };
    process(1);
    verify_events();
}
