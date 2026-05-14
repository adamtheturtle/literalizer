#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"title" = "report",
	"tags" = [dynamic]any{"draft", "urgent", "review"},
	"priority" = 2,
}
_ = my_data
}
