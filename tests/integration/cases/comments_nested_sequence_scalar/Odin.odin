#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{"ADD", "alice", "hello"},
	[dynamic]any{"DEL", "bob", "5"},  // removes "world"
}
_ = my_data
}
