#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"i32_below" = -0o20000000001,
	"i32_minimum" = -0o20000000000,
	"i32_above" = -0o17777777777,
	"i32_maximum" = 0o17777777777,
	"i32_over" = 0o20000000000,
	"i64_minimum" = -0o1000000000000000000000,
	"i64_maximum" = 0o777777777777777777777,
}
_ = my_data
}
