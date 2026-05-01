package main

func main() {
var my_data = [][]string{
	[]string{"ADD", "alice", "hello"},
	[]string{"DEL", "bob", "5"},  // removes "world"
}
my_data = [][]string{
	[]string{"ADD", "alice", "hello"},
	[]string{"DEL", "bob", "5"},  // removes "world"
}
_ = my_data
}
