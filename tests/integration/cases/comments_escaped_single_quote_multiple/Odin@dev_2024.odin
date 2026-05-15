#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"host" = "it's here",  // a comment
	"port" = 80,  // another
}
_ = my_data
}
