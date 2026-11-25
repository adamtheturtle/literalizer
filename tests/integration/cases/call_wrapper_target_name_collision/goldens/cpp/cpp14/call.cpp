template <typename... Args> auto check(Args...) { return 0; }
int main() {
check(42);
    return 0;
}
