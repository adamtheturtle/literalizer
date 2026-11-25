fn main() {
    let event_index = std::cell::Cell::new(0_usize);
    let observe_event = |actual: i32| {
        let expected = [1, -1, 1, -2, 1, -3];
        let index = event_index.get();
        assert!(index < 6);
        assert_eq!(actual, expected[index]);
        event_index.set(index + 1);
    };
    let process = |value: i32| { observe_event(1); observe_event(value); value + 100 };
    let verify_events = || { assert_eq!(event_index.get(), 6); };
    process(-1);
    process(-2);
    process(-3);
    verify_events();
}
