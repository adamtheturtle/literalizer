template <typename... Args> auto check_wrapper(Args...) { return 0; }
int main() {
check_wrapper(42);
    return 0;
}
