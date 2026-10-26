template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto value = 1;
process(value);
    return 0;
}
