template <typename... Args> auto process(Args...) { return 0; }
struct helpersType_ { template <typename... Args> void emit(Args...) const {} };
const helpersType_ helpers;
int main() {
helpers.emit(process(1), 42);
    return 0;
}
