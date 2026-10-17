struct Playlist { int value = 42; }

void main() {
let p = Playlist::new();
assert(p.value == 42);
}
