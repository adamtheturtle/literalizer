typedef int CVal;

CVal Playlist(void) { return 42; }

int main(void) {
static Object playlist = new Playlist();
return playlist == 42 ? 0 : 1;
}
