struct Playlist { int value = 42; };

int main() {
final Object playlist = new Playlist();
return playlist.value == 42 ? 0 : 1;
}
