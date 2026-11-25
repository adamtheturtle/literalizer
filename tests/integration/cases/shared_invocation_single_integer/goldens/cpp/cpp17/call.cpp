template <typename... Args> auto consume(Args...) { return 0; }
int main() {
consume(1);
    return 0;
}
