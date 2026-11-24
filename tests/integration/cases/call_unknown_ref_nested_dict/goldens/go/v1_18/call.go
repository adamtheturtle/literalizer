package main
func process(args ...any) any { return nil }

func main() {
my_list := map[string]string{
	"unused": "value",
}
process([][]map[string]map[string]string{[]map[string]map[string]string{{"inner": my_list}}})
}
