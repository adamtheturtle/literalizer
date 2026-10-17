struct Playlist { int value = 42; }

void main() {
(defparameter *p* (Playlist))
assert(p.value == 42);
}
