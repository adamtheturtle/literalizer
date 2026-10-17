struct Playlist { int value = 42; };

int main() {
static Object playlist = new Playlist();
return playlist.value == 42 ? 0 : 1;
}
