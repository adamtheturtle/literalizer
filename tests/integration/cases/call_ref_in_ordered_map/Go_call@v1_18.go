package main
func process(args ...any) any { return nil }

func main() {
big_list := []string{
	"x",
}
process([][2]any{{"m", big_list}})
}
