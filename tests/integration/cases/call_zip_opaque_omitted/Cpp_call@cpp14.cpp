template <typename... Args> auto process(Args...) { return 0; }
int main() {
static_cast<void>(process(1));
    return 0;
}
