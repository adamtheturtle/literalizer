fn main() {
    let event_index = std::cell::Cell::new(0_usize);
    let observe_event = |actual: i32| {
        let expected = [1, 42];
        let index = event_index.get();
        assert!(index < 2);
        assert_eq!(actual, expected[index]);
        event_index.set(index + 1);
    };
    let f = |a: i32| { observe_event(1); observe_event(a); a + 100 };
    let verify_events = || { assert_eq!(event_index.get(), 2); };
    // scalar heading
    // second heading line
    // scalar inline
    // inline continuation
    // scalar trailing
    f(42);
    verify_events();
}
