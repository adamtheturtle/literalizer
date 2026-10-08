#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	/* nested openers /* and {- remain */
	"x" = 1,
}
_ = my_data
}
