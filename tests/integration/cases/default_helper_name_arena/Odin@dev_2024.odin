#+feature dynamic-literals
package main

main :: proc() {
arena := map[string]any{
	"a" = 1,
}
_ = arena
}
