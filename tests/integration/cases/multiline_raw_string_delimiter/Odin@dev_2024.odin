#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"custom base after empty collision: )\"\nvalue",
	"custom suffix after base collision: )\" and )x0\"\nvalue",
	"custom second suffix: )\" and )x0\" and )x00\"\nvalue",
	"long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue",
}
_ = my_data
}
