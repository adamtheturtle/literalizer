#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 1,  // tab	here and bidi <U+202E>after
	"b" = 2,
}
_ = my_data
}
