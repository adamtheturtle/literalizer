#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"v" = "a‪‫‬‭‮⁦⁧⁨⁩b",
}
_ = my_data
}
