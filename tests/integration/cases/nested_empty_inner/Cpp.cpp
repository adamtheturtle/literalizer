#include <initializer_list>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::vector<std::vector<std::monostate>>{
    std::vector<std::monostate>{},
    std::vector<std::monostate>{},
};
}
