#+feature dynamic-literals
package main

main :: proc() {
key_binding := map[string]any{
	"a" = 1,
}
_ = key_binding
}
