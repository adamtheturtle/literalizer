package main

var _ = map[any]struct{}{
    "apple": struct{}{},  // inline comment
    // before banana
    "banana": struct{}{},
    // trailing
}
