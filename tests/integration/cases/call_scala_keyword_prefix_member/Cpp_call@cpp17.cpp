#include <initializer_list>
#include <vector>
struct PlaylistType_ { template <typename... Args> void newValue(Args...) const {} };
const PlaylistType_ Playlist;
int main() {
Playlist.newValue(1);
    return 0;
}
