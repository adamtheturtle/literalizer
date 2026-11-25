#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"metrics" = map[string]any{"count" = 100, "rate" = 50},
	"flags" = map[string]any{"retries" = 3, "timeout" = 30},
}
_ = my_data
}
