struct Record0 { int a{}; };
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto item = Record0{
    1,
};
const auto* stamp = "2001-02-03";
consume(stamp, item);
    return 0;
}
