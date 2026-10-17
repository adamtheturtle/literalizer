struct Playlist { int value = 42; }

void main() {
final Object p = new Playlist();
assert(p.value == 42);
}
