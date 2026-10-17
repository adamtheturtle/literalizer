#include <initializer_list>
#include <vector>
#include <cstddef>
auto Playlist(auto...) { return 0; }
int main() {
auto created = Playlist();
    (void)created;
    return 0;
}
