#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
using LiteralizerRecordValue = std::variant<int, std::string>;
struct Record0 { std::map<std::string, LiteralizerRecordValue> input; };
int main() {
auto my_data = std::vector{
    Record0{.input = {{"a", LiteralizerRecordValue{1}}}},
    Record0{.input = {{"b", LiteralizerRecordValue{"two"}}}},
};
    (void)my_data;
    return 0;
}
