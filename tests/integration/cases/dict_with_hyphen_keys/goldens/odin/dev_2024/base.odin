#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"my-key" = "value1",
	"another-key" = "value2",
	"normal_key" = "value3",
}
_ = my_data
}
