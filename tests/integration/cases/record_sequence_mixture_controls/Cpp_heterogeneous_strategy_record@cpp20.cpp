#include <cstddef>
#include <variant>
#include <vector>
struct Record0 { int x{}; };
int main() {
auto my_data = std::vector<std::variant<std::vector<std::variant<std::vector<int>, Record0>>, std::vector<Record0>, std::vector<std::vector<Record0>>, std::vector<std::vector<std::nullptr_t>>>>{
    std::vector<std::variant<std::vector<int>, Record0>>{std::vector<int>{1}, Record0{.x = 1}},
    std::vector{Record0{.x = 1}, Record0{.x = 2}},
    std::vector{std::vector<Record0>{}, std::vector{Record0{.x = 1}}},
    std::vector<std::vector<std::nullptr_t>>{std::vector<std::nullptr_t>{}, std::vector<std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
