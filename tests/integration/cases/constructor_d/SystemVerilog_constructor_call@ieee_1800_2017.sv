struct Playlist { int value = 42; }

void main() {
static _VVal p = Playlist();
assert(p.value == 42);
}
