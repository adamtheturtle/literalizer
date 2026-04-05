#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"key\nwith\nnewlines" = "value1",
	"key\twith\ttabs" = "value2",
	"" = "value3",
}
_ = my_data
}
