#+feature dynamic-literals
package main
Playlist :: proc(args: ..any) -> any { return nil }

main :: proc() {
created := Playlist()
_ = created
}
