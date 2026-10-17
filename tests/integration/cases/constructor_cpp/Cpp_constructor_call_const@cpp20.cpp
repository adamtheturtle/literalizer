struct Playlist { int value = 42; };

int main() {
const auto playlist = Playlist();
return playlist.value == 42 ? 0 : 1;
}
