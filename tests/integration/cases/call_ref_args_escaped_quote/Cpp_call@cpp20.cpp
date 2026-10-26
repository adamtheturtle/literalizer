auto process(auto...) { return 0; }
int main() {
const auto* my_str = "a\"b";
process(my_str);
    return 0;
}
