#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// server
	"host" = "localhost",  // default
}
_ = my_data
}
