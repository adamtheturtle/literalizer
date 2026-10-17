struct Playlist { int value = 42; }

void main() {
declare p="$(Playlist)"
assert(p.value == 42);
}
