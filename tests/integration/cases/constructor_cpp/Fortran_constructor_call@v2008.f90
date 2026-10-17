struct Playlist { int value = 42; };

int main() {
type(fval_t) :: playlist
playlist = Playlist()
return playlist.value == 42 ? 0 : 1;
}
