Playlist() { printf '%s\n' 42; }

my $p = Playlist();
[[ "$p" == 42 ]] || exit 1
