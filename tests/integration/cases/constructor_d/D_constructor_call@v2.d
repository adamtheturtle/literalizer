struct Playlist { int value = 42; }

void main() {
auto p = Playlist();
assert(p.value == 42);
}
