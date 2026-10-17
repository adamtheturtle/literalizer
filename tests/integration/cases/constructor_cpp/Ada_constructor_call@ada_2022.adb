struct Playlist { int value = 42; };

int main() {
playlist : A_Val := Playlist;
return playlist.value == 42 ? 0 : 1;
}
