#+feature dynamic-literals
package main

main :: proc() {
allocator := map[string]any{
	"a" = 1,
}
_ = allocator
}
