#+feature dynamic-literals
package main

main :: proc() {
item := [dynamic]any{
	1,
	2,
}
my_data := [dynamic]any{
	1,
	2,
}
(void)my_data;
my_data = item
(void)my_data;
}
