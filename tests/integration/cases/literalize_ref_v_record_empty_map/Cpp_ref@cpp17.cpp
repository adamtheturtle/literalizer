#include <initializer_list>
#include <string>
#include <map>
#include <cstddef>
#include <variant>
struct Record0 { std::map<std::string, std::nullptr_t> bound; };
int main() {
auto empty_map = std::map<std::string, std::nullptr_t>{};
auto my_data = Record0{
    std::move(empty_map),
};
    (void)my_data;
    return 0;
}
