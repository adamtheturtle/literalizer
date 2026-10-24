#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a_b" = 0x1,
	"a-b" = 0x2,
	"averyveryverylongkeynamethatgoesonandonandon" = 0x3,
	"averyveryverylongkeynamethatgoesonandmore" = 0x4,
}
_ = my_data
}
