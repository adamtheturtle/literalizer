#+feature dynamic-literals
package main
do_thing :: proc(args: ..any) -> any { return nil }

main :: proc() {
do_thing(1);
do_thing(2);
}
