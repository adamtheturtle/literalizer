#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"date" = "0099-05-27",
	"naive" = -62135551800,
	"recent" = 1716804000,
}
_ = my_data
}
