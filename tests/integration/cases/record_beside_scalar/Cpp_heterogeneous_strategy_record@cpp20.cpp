#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record0 { int a{}; };
int main() {
auto my_data = std::vector<std::variant<Record0, int>>{
    Record0{.a = 1},
    5,
};
    (void)my_data;
    return 0;
}
