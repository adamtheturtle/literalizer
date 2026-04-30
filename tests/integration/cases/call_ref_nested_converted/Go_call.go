package main
func process(args ...any) any { return nil }

func main() {
MyVar := 42
process([]any{map[string]string{"ref": "myVar"}, 42, "static"});
}
