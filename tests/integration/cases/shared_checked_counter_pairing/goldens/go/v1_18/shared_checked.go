package main
type Counter struct { calls int }
func (c *Counter) accept(user string, timestamp float64) bool {
    wanted := "user_1"
    if c.calls != 0 { wanted = "user_2" }
    if user != wanted || timestamp != 100.0 + float64(c.calls) { panic("receiver arguments changed") }
    c.calls++
    return user == "user_1"
}
var checks int
func checkResult(actual bool, expected []any) {
    reason := "first"
    if checks != 0 { reason = "second" }
    if actual != expected[0].(bool) || expected[1].(string) != reason { panic("paired result changed") }
    checks++
}
func main() {
    counter := Counter{}
	checkResult(counter.accept("user_1", 100.0), []any{true, "first"})
	checkResult(counter.accept("user_2", 101.0), []any{false, "second"})
    if counter.calls != 2 || checks != 2 { panic("calls skipped") }
}
