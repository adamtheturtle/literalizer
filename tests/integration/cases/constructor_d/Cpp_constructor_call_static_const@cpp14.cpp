struct Playlist { int value = 42; }

void main() {
static const auto p = Playlist();
assert(p.value == 42);
}
