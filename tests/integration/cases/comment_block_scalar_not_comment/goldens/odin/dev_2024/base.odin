#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"description" = "# not a comment\n",
	"name" = "foo",
}
_ = my_data
}
