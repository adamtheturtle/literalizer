package main

main :: proc() {
my_data := map[string]struct{}{
	true = {},
	42 = {},
	"apple" = {},
}
_ = my_data
}
