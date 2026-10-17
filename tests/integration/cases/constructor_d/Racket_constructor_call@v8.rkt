struct Playlist { int value = 42; }

void main() {
(define p (Playlist))
assert(p.value == 42);
}
