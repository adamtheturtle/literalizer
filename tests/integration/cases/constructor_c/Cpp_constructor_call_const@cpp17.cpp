typedef int CVal;

CVal Playlist(void) { return 42; }

int main(void) {
const auto playlist = Playlist();
return playlist == 42 ? 0 : 1;
}
