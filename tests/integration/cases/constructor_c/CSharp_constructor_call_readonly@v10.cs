typedef int CVal;

CVal Playlist(void) { return 42; }

int main(void) {
readonly object? playlist = new Playlist();
return playlist == 42 ? 0 : 1;
}
