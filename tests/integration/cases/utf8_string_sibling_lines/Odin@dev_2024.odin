#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"中中中中中中中中中中中中中中中中中中中中",
	"é'é'é'é'é'é'é'é'é'é'",
	"🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂",
}
_ = my_data
}
