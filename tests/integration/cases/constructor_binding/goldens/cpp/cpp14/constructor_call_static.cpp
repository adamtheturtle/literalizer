template <typename... Args> auto Playlist(Args...) { return 0; }
int main() {
static auto created = Playlist();
    (void)created;
    return 0;
}
