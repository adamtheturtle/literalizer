#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"ts" = "3000-12-31T23:59:59.999999+00:00",
}
my_data = map[string]any{
	"ts" = "3000-12-31T23:59:59.999999+00:00",
}
_ = my_data
}
