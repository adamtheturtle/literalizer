struct Playlist { int value = 42; }

void main() {
var p = Playlist.new()
assert(p.value == 42);
}
