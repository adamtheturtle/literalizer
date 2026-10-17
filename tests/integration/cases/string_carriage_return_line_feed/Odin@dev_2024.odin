#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"cr" = "a\rb",
	"crlf" = "a\r\nb",
	"lf" = "a\nb",
}
_ = my_data
}
