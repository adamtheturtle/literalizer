#+feature dynamic-literals
package main
check :: proc(args: ..any) -> any { return nil }

main :: proc() {
check("2024-01-15T10:30:00+00:00", "2024-06-01");
}
