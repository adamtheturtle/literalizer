package main

func main() {
my_data := map[string]string{
	`cr`: "a\rb",
	`crlf`: "a\r\nb",
	`lf`: `a
b`,
}
_ = my_data
}
