class Thing_ {
    construct new() {}
    go(before, populated, after) {}
}
var thing = Thing_.new()
thing.go([], [1], [])
thing.go(["text"], [2], [])
thing.go([], ["text"], [])
thing.go(["text"], [2], [3])
