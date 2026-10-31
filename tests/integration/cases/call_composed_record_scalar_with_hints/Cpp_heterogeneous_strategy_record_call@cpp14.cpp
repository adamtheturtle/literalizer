struct Record0 { int a{}; };
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto item = Record0{
    1,
};
consume(item);
    return 0;
}
