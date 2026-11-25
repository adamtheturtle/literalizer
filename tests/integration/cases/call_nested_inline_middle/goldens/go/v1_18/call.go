package main
func f(args ...any) any { return nil }

func main() {
f([][]string{[]string{"DEL", "b", "10"}, []string{"ADD", "a", "x"}})  // note
// next call
f([][]string{[]string{"ADD", "c", "y"}})
}
