struct Playlist { int value = 42; };

int main() {
set playlist [Playlist]
return playlist.value == 42 ? 0 : 1;
}
