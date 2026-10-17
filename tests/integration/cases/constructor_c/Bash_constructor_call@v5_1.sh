typedef int CVal;

CVal Playlist(void) { return 42; }

int main(void) {
declare playlist="$(Playlist)"
return playlist == 42 ? 0 : 1;
}
