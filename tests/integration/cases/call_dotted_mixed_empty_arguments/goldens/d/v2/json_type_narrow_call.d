void main() {
struct ThingType_ { int go(T...)(T args) { return 0; } }
ThingType_ thing;
thing.go([], [1], []);
thing.go(["text"], [2], []);
thing.go([], ["text"], []);
thing.go(["text"], [2], [3]);
}
