#include <initializer_list>
#include <vector>
struct PlaylistType_ { template <typename... Args> void new(Args...) const {} };
const PlaylistType_ Playlist;
int main() {
Playlist.new(1);
    return 0;
}
