typedef int CVal;

CVal Playlist(void) { return 42; }

int main(void) {
(define playlist (Playlist))
return playlist == 42 ? 0 : 1;
}
