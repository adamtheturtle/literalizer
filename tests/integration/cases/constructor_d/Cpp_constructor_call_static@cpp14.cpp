struct Playlist { int value = 42; }

void main() {
static auto p = Playlist();
assert(p.value == 42);
}
