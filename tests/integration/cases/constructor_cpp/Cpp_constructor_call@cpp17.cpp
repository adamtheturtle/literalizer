#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Args> auto Playlist(Args...) { return 0; }
int main() {
auto playlist = Playlist();
    (void)playlist;
    return 0;
}
