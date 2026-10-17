#include <initializer_list>
#include <vector>
#include <cstddef>
auto Playlist(auto...) { return 0; }
int main() {
const auto playlist = Playlist();
    (void)playlist;
    return 0;
}
