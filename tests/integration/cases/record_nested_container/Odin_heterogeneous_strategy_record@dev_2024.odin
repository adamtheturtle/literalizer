#+feature dynamic-literals
package main
Record0 :: struct { title: string, tags: [dynamic]any, priority: int }

main :: proc() {
my_data := Record0{
	title = "report",
	tags = [dynamic]any{
		"draft",
		"urgent",
		"review",
	},
	priority = 2,
}
_ = my_data
}
