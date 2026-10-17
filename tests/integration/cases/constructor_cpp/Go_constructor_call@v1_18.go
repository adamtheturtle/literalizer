struct Playlist { int value = 42; };

int main() {
playlist := NewPlaylist()
return playlist.value == 42 ? 0 : 1;
}
