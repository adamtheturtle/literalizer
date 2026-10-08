#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto one = 1;
const auto* two = "s";
auto my_data = std::vector<std::variant<int, std::string>>{
    one,
    std::move(two),
};
    (void)my_data;
    return 0;
}
