template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto value = nullptr;
consume(value);
    return 0;
}
