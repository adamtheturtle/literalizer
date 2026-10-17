struct Playlist { int value = 42; }

void main() {
const auto p = Playlist();
assert(p.value == 42);
}
