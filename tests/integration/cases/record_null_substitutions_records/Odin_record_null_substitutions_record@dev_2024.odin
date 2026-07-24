#+feature dynamic-literals
package main
Record0 :: struct { due_date: int, parent_id: int, assignee: string }

main :: proc() {
my_data := [dynamic]any{
	Record0{ due_date = -1, parent_id = -1, assignee = "" },
	Record0{ due_date = 10, parent_id = 20, assignee = "alice" },
}
_ = my_data
}
