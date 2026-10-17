struct Playlist { int value = 42; }

void main() {
type(fval_t) :: p
p = Playlist()
assert(p.value == 42);
}
