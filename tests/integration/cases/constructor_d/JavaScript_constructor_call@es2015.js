struct Playlist { int value = 42; }

void main() {
const p = new Playlist({  });
assert(p.value == 42);
}
