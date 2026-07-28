#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto known_value = true;
auto unknown_value = true;
process(known_value, std::vector<std::map<std::string, std::string>>{unknown_value});
    return 0;
}
