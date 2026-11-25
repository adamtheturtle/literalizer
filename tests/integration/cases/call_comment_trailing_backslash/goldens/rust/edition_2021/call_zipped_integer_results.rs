fn main() {
    let event_index = std::cell::Cell::new(0_usize);
    let observe_event = |actual: i32| {
        let expected = [1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42];
        let index = event_index.get();
        assert!(index < 12);
        assert_eq!(actual, expected[index]);
        event_index.set(index + 1);
    };
    let process = |value: i32| { observe_event(1); observe_event(value); value + 100 };
    let emit = |actual: i32, zipped: i32| { observe_event(2); observe_event(actual); observe_event(3); observe_event(zipped); };
    let verify_events = || { assert_eq!(event_index.get(), 12); };
    emit(process(1), 41);
    emit(process(2), 42);
    verify_events();
}
