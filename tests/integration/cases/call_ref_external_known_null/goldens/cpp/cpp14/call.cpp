template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto item = nullptr;
consume(item);
    return 0;
}
