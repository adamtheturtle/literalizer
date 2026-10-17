typedef int CVal;

CVal Playlist(void) { return 42; }

int main(void) {
let mut playlist = Playlist::new();
return playlist == 42 ? 0 : 1;
}
