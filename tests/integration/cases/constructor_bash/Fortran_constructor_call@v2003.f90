Playlist() { printf '%s\n' 42; }

type(fval_t) :: p
p = Playlist()
[[ "$p" == 42 ]] || exit 1
