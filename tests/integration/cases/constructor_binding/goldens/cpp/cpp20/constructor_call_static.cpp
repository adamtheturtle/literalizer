auto Playlist(auto...) { return 0; }
int main() {
static auto created = Playlist();
    (void)created;
    return 0;
}
