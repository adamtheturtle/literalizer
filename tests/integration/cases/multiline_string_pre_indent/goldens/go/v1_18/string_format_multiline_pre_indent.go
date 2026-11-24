package main
func main() {
	my_data := `
first line
  indented

last line
`
    if my_data != "\nfirst line\n  indented\n\nlast line\n" { panic("changed multiline string") }
}
