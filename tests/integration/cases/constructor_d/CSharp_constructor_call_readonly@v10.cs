struct Playlist { int value = 42; }

void main() {
readonly object? p = new Playlist();
assert(p.value == 42);
}
