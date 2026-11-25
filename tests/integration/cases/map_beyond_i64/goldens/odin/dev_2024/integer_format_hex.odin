#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 0x7fffffffffffffff,
	"b" = u64(0x8000000000000000),
}
_ = my_data
}
