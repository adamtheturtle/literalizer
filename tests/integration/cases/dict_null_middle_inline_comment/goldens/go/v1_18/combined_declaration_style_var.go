package main

func main() {
var my_data = map[string]map[string]any{
	"server": map[string]any{
		"host": "localhost",
		"port": nil,  // not configured yet
		"debug": true,
	},
}
my_data = map[string]map[string]any{
	"server": map[string]any{
		"host": "localhost",
		"port": nil,  // not configured yet
		"debug": true,
	},
}
_ = my_data
}
