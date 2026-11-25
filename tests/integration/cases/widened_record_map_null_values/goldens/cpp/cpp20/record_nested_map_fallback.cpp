#include <vector>
#include <cstddef>
#include <map>
#include <string>
struct Record0 { std::map<std::string, std::nullptr_t> input; };
int main() {
auto my_data = std::vector{
    Record0{.input = {{"a", nullptr}}},
    Record0{.input = {{"b", nullptr}}},
};
    (void)my_data;
    return 0;
}
