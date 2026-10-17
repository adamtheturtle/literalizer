struct Playlist { int value = 42; };

int main() {
public static readonly object? playlist = new Playlist();
return playlist.value == 42 ? 0 : 1;
}
