template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("hello");
process(42);
process(true);
    return 0;
}
