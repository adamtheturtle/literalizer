package main
func f(args ...any) any { return nil }
func repr(args ...any) any { return nil }

func main() {
ref_data := 1
repr(f(ref_data))
}
