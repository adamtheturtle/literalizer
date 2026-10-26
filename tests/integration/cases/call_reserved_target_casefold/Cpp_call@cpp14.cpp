template <typename... Args> auto BEGIN(Args...) { return 0; }
int main() {
BEGIN(42);
    return 0;
}
