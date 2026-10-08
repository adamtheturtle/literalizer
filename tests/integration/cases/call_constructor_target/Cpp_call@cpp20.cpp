#include <initializer_list>
#include <vector>
struct PlaylistType_ { void new(auto...) const {} };
const PlaylistType_ Playlist;
int main() {
Playlist.new(1);
    return 0;
}
