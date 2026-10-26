#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, std::map<std::string, std::nullptr_t>>>{
    1,
    std::map<std::string, std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
