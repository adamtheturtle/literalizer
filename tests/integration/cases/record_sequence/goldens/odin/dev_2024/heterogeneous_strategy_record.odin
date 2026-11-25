#+feature dynamic-literals
package main
Record0 :: struct { id: int, label: string, tags: [dynamic]any }

main :: proc() {
my_data := [dynamic]any{
	Record0{ id = 1, label = "first", tags = [dynamic]any{} },
	Record0{ id = 2, label = "second", tags = [dynamic]any{} },
	Record0{ id = 3, label = "third", tags = [dynamic]any{} },
}
_ = my_data
}
