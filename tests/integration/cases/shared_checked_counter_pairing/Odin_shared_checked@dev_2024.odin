#+feature dynamic-literals
package main
calls, checks: int
accept :: proc(user: string, timestamp: f64) -> bool {
    assert(user == (calls == 0 ? "user_1" : "user_2"))
    assert(timestamp == 100.0 + f64(calls))
    calls += 1
    return user == "user_1"
}
checkResult :: proc(actual: bool, expected: [dynamic]any) {
    assert(actual == expected[0].(bool))
    assert(expected[1].(string) == (checks == 0 ? "first" : "second"))
    checks += 1
}
main :: proc() {
    counter := struct { accept: proc(string, f64) -> bool }{accept}
	checkResult(counter.accept("user_1", 100.0), [dynamic]any{true, "first"});
	checkResult(counter.accept("user_2", 101.0), [dynamic]any{false, "second"});
    assert(calls == 2 && checks == 2)
}
