#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a_b" = 0o1,
	"a-b" = 0o2,
	"averyveryverylongkeynamethatgoesonandonandon" = 0o3,
	"averyveryverylongkeynamethatgoesonandmore" = 0o4,
}
_ = my_data
}
