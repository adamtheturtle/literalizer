#+feature dynamic-literals
package main

main :: proc() {
k := map[string]any{
	"a" = 1,
}
_ = k
}
