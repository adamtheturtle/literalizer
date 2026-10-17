struct Playlist { int value = 42; }

void main() {
(def p (Playlist))
assert(p.value == 42);
}
