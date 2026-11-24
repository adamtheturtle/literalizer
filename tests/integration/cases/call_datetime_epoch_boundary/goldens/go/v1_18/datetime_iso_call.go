package main
func consume(args ...any) any { return nil }

func main() {
consume("1901-12-13T20:45:51")
consume("2038-01-19T03:14:08")
}
