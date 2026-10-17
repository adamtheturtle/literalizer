struct Playlist { int value = 42; }

void main() {
CVal p = Playlist();
assert(p.value == 42);
}
