struct Playlist { int value = 42; };

int main() {
local playlist = Playlist()
return playlist.value == 42 ? 0 : 1;
}
