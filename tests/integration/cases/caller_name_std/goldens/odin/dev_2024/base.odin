#+feature dynamic-literals
package main

main :: proc() {
std := map[string]any{
	"a" = 1,
}
_ = std
}
