#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
	1,
}
_ = my_data
}
