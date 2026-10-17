typedef int CVal;

CVal Playlist(void) { return 42; }

int main(void) {
private object? playlist = new Playlist();
return playlist == 42 ? 0 : 1;
}
