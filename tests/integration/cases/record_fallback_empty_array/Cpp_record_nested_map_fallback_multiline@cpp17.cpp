#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
using LiteralizerRecordValue = std::variant<int, std::vector<std::nullptr_t>>;
struct Record0 { std::string name; std::map<std::string, LiteralizerRecordValue> payload; };
int main() {
auto my_data = std::vector{
    Record0{
        "one",
        {
            {"scalar", LiteralizerRecordValue{1}},
            {"items", std::vector<std::nullptr_t>{}},
        },
    },
    Record0{
        "two",
        {
            {"other", LiteralizerRecordValue{2}},
        },
    },
};
    (void)my_data;
    return 0;
}
