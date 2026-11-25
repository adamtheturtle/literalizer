template <typename... Args> auto process(Args...) { return 0; }
int main() {
static_cast<void>(process("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)"));
    return 0;
}
