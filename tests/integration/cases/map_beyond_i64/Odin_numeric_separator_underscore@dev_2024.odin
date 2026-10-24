#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 9_223_372_036_854_775_807,
	"b" = u64(9_223_372_036_854_775_808),
}
_ = my_data
}
