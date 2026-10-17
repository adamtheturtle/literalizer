struct Playlist { int value = 42; };

int main() {
CVal playlist = Playlist();
return playlist.value == 42 ? 0 : 1;
}
