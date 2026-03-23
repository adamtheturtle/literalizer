package main

var _ = map[string]struct{}{
    "apple": struct{}{},  // inline comment
    // before banana
    "banana": struct{}{},
    // trailing
}
