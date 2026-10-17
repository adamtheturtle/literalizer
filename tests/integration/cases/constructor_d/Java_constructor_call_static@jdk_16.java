struct Playlist { int value = 42; }

void main() {
static Object p = new Playlist();
assert(p.value == 42);
}
