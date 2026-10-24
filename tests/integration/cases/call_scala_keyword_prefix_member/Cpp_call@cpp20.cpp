#include <initializer_list>
#include <vector>
struct PlaylistType_ { void newValue(auto...) const {} };
const PlaylistType_ Playlist;
int main() {
Playlist.newValue(1);
    return 0;
}
