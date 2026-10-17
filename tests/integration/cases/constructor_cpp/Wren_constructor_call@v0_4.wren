struct Playlist { int value = 42; };

int main() {
var playlist = Playlist.new()
return playlist.value == 42 ? 0 : 1;
}
