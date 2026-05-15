#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// before
	"answer" = 42,  // inline
	"plain" = "ok",
	// trailing
}
_ = my_data
}
