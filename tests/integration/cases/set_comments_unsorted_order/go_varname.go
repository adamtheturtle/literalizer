package main

func main() {
my_data := map[any]struct{}{
    // before apple
    "apple": struct{}{},
    "banana": struct{}{},  // banana inline
    // trailing
}
_ = my_data
}
