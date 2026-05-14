#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// Configuration
	"name" = "app",
	// Port setting
	"port" = 3000,
}
_ = my_data
}
