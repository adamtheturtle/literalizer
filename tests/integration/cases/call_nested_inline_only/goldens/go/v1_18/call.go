package main
func f(args ...any) any { return nil }

func main() {
f(2, "hello")  // trailing note
f(3, "world")  // another note
}
