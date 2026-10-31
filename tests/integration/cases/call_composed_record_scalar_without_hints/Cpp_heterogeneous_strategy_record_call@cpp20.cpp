struct Record0 { int a{}; };
auto consume(auto...) { return 0; }
int main() {
auto item = Record0{
    .a = 1,
};
consume(item);
    return 0;
}
