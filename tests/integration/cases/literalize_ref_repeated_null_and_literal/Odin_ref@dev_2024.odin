#+feature dynamic-literals
package main

main :: proc() {
value: any = nil
my_data := [dynamic]any{
	value,
	value,
	nil,
}
_ = my_data
}
