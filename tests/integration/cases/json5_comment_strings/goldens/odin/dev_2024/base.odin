#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	// strings stay data
	"https://example.org/a/*b*/",  // URL annotation
	"escaped quote: \" // still data",
	"backslash: \\",  // outside the string
	"/* not a comment */",
}
_ = my_data
}
