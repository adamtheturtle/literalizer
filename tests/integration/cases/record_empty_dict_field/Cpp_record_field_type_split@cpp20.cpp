#include <initializer_list>
#include <string>
#include <map>
#include <cstddef>
#include <variant>
struct Record0 { std::map<std::string, std::nullptr_t> f; int g{}; };
int main() {
auto my_data = Record0{
    .f = std::map<std::string, std::nullptr_t>{},
    .g = 1,
};
    (void)my_data;
    return 0;
}
