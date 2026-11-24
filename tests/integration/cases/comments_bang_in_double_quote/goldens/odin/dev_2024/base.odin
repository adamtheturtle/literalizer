#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"key" = "\"bang!\"",  // real
}
_ = my_data
}
