package main
func consume(args ...any) any { return nil }

func main() {
foo := 42
consume([]map[string]int{
	{
		"other": 1,
	},
	foo,
}, map[string]int{
	"left": foo,
	"other": 1,
})
}
