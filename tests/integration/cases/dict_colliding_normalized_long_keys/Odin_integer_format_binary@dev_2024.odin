#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a_b" = 0b1,
	"a-b" = 0b10,
	"averyveryverylongkeynamethatgoesonandonandon" = 0b11,
	"averyveryverylongkeynamethatgoesonandmore" = 0b100,
}
_ = my_data
}
