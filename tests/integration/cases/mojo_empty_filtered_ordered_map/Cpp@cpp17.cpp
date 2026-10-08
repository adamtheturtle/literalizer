#include <initializer_list>
#include <string>
#include <cstddef>
#include <utility>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::pair<std::string, std::nullptr_t>>{
    {"missing", nullptr},
};
    (void)my_data;
    return 0;
}
