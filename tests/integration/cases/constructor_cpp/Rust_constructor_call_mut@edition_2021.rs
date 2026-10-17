struct Playlist { int value = 42; };

int main() {
let mut playlist = Playlist::new();
return playlist.value == 42 ? 0 : 1;
}
