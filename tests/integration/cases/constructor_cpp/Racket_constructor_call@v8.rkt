struct Playlist { int value = 42; };

int main() {
(define playlist (Playlist))
return playlist.value == 42 ? 0 : 1;
}
