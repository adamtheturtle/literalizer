package main

func main() {
my_data := map[string]any{
    "key\nwith\nnewlines": "value1",
    "key\twith\ttabs": "value2",
}
_ = my_data
}
