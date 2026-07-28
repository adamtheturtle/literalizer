package main
func process(args ...any) any { return nil }

func main() {
my_list := []any{}
process([][]map[string]map[string]string{[]map[string]map[string]string{{"inner": my_list}}})
}
