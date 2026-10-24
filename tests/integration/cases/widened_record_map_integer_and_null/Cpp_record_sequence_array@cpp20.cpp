#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <array>
#include <variant>
#include <vector>
using LiteralizerRecordValue = std::variant<int, std::nullptr_t>;
struct Record0 { std::map<std::string, LiteralizerRecordValue> input; };
int main() {
auto my_data = std::vector{
    Record0{.input = {{"a", LiteralizerRecordValue{1}}}},
    Record0{.input = {{"b", LiteralizerRecordValue{nullptr}}}},
};
    (void)my_data;
    return 0;
}
