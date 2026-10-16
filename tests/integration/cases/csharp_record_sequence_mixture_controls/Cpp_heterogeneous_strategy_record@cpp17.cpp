#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
struct Record0 { int x{}; };
int main() {
auto my_data = std::vector<std::variant<std::vector<std::variant<std::vector<int>, Record0>>, std::vector<Record0>, std::vector<std::vector<Record0>>, std::vector<std::vector<std::nullptr_t>>>>{
    std::vector<std::variant<std::vector<int>, Record0>>{std::vector<int>{1}, Record0{1}},
    std::vector{Record0{1}, Record0{2}},
    std::vector{std::vector<Record0>{}, std::vector{Record0{1}}},
    std::vector<std::vector<std::nullptr_t>>{std::vector<std::nullptr_t>{}, std::vector<std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
