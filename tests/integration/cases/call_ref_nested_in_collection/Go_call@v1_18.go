package main
func process(args ...any) any { return nil }

func main() {
big_list := []string{
	"x",
}
process(map[string][]string{"k": big_list}, 2)
}
