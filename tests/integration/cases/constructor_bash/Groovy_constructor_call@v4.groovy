Playlist() { printf '%s\n' 42; }

def p = new Playlist()
[[ "$p" == 42 ]] || exit 1
