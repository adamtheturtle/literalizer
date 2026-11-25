#include <string>
struct Record0 { int a{}; std::string b; };
template <typename... Args> auto consume_widget(Args...) { return 0; }
int main() {
consume_widget(Record0{
    1,
    "x",
});
    return 0;
}
