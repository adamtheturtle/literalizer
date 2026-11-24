auto Playlist(auto...) { return 0; }
int main() {
static const auto created = Playlist();
    (void)created;
    return 0;
}
