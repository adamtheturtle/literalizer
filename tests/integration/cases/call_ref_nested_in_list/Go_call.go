package main
func process(args ...any) any { return nil }

func main() {
my_var := 42
my_other := 7
process([]any{my_var, 42, "static"});
process([]any{my_other, 7, "label"});
}
