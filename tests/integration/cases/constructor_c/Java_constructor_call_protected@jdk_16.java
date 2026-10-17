typedef int CVal;

CVal Playlist(void) { return 42; }

int main(void) {
protected Object playlist = new Playlist();
return playlist == 42 ? 0 : 1;
}
