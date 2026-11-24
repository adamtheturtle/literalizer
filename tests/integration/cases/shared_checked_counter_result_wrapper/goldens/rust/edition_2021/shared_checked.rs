
use std::cell::Cell;
struct Counter { calls: Cell<usize> }
impl Counter {
    fn accept(&self, user: &str, timestamp: f64) -> bool {
        let calls = self.calls.get();
        assert_eq!(user, if calls == 0 { "user_1" } else { "user_2" });
        assert_eq!(timestamp, 100.0 + calls as f64);
        self.calls.set(calls + 1);
        user == "user_1"
    }
}
fn main() {
    let counter = Counter { calls: Cell::new(0) };
    let checks = Cell::new(0);
    let check_result = |actual: bool, expected: (bool, &str)| {
        assert_eq!(actual, expected.0);
        assert_eq!(expected.1, if checks.get() == 0 { "first" } else { "second" });
        checks.set(checks.get() + 1);
    };
    check_result(counter.accept("user_1", 100.0), (true, "first"));
    assert_eq!(counter.calls.get(), 1);
    assert_eq!(checks.get(), 1);
}
