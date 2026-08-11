#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a_b" = 1,
	"a-b" = 2,
	"averyveryverylongkeynamethatgoesonandonandon" = 3,
	"averyveryverylongkeynamethatgoesonandmore" = 4,
}
_ = my_data
}
