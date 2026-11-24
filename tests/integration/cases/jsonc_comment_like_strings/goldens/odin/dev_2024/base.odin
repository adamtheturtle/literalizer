#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"// data",
	"/* data */",
	"escaped quote: \" // data",
	"backslash: \\",
}
_ = my_data
}
