#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	/* "{-" and '{-' stay readable */
	/* balanced {- nested -} and trailing -} stay readable */
	"x" = 1,
}
_ = my_data
}
