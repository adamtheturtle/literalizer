#+feature dynamic-literals
package main

main :: proc() {
ref_data := [dynamic]any{
	1,
	2,
}
my_data := [dynamic]any{
	0,
}
(void)my_data;
my_data = ref_data
(void)my_data;
}
