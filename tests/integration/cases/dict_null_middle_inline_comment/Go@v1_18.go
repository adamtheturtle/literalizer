package main

func main() {
my_data := map[string]map[string]any{
	"server": map[string]any{
		"host": "localhost",
		"port": nil,  // not configured yet
		"debug": true,
	},
}
_ = my_data
}
