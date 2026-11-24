template <typename... Args> auto process(Args...) { return 0; }
template <typename... Args> auto emit(Args...) { return 0; }
int main() {
emit(process(1), "2024-01-15T12:00:00");
    return 0;
}
