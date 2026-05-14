#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"host" = "localhost",
	"port" = nil,  // not configured yet
	"debug" = true,
}
_ = my_data
}
