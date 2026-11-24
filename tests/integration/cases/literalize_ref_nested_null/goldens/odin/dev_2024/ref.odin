#+feature dynamic-literals
package main

main :: proc() {
my_null: any = nil
my_data := [dynamic]any{
	my_null,
	nil,
}
_ = my_data
}
