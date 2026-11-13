interface IVal {}
struct Counter { mut: calls int }
fn (mut counter Counter) accept(user string, timestamp f64) bool {
    assert user == if counter.calls == 0 { 'user_1' } else { 'user_2' }
    assert timestamp == 100.0 + f64(counter.calls)
    counter.calls++
    return user == 'user_1'
}
struct Checker { mut: calls int }
fn (mut checker Checker) check_result(actual bool, expected []IVal) {
    assert actual == (expected[0] as bool)
    assert (expected[1] as string) == if checker.calls == 0 { 'first' } else { 'second' }
    checker.calls++
}
fn main() {
    mut counter := Counter{}
    mut checker := Checker{}
	checker.check_result(counter.accept('user_1', 100.0), [IVal(true), IVal('first')]);
	checker.check_result(counter.accept('user_2', 101.0), [IVal(false), IVal('second')]);
    assert counter.calls == 2
    assert checker.calls == 2
}
