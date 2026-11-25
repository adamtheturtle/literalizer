#include <string>
struct Record0 { int a{}; std::string b; };
auto consume_widget(auto...) { return 0; }
int main() {
consume_widget(Record0{
    .a = 1,
    .b = "x",
});
    return 0;
}
