struct Playlist { int value = 42; };

int main() {
static _VVal playlist = Playlist();
return playlist.value == 42 ? 0 : 1;
}
