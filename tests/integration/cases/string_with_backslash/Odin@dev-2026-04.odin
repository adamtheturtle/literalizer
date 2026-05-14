#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"C:\\path\\to\\file",
	"back\\\\slash",
	"hello \\\"world\\\"",
	"path\\to \"# file",
	"trailing\\",
	"both \"quotes''' here",
	"line1\\nline2\nwith newline",
}
_ = my_data
}
