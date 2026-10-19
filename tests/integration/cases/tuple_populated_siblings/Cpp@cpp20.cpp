#include <initializer_list>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::variant<int, std::vector<int>>>>{
    std::vector<std::variant<int, std::vector<int>>>{1, std::vector<int>{2}},
    std::vector<std::variant<int, std::vector<int>>>{3, std::vector<int>{4}},
};
    (void)my_data;
    return 0;
}
