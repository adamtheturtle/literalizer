auto process(auto...) { return 0; }
struct helpersType_ { void emit(auto...) const {} };
const helpersType_ helpers;
int main() {
helpers.emit(process(1), 42);
    return 0;
}
