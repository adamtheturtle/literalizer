#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 0o777777777777777777777,
	"b" = u64(0o1000000000000000000000),
}
_ = my_data
}
