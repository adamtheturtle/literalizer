struct Playlist { int value = 42; }

void main() {
set p [Playlist]
assert(p.value == 42);
}
