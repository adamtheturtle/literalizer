struct Record0 { int a{}; };
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
const auto* stamp = "2001-02-03";
auto item = Record0{
    1,
};
consume(stamp, item);
    return 0;
}
