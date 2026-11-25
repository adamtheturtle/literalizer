template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("a\"b");
    return 0;
}
