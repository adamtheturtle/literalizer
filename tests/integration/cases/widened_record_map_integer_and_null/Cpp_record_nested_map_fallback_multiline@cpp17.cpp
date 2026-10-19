#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <variant>
using LiteralizerRecordValue = std::variant<int, std::nullptr_t>;
struct Record0 { std::map<std::string, LiteralizerRecordValue> input; };
int main() {
auto my_data = std::vector{
    Record0{
        {
            {"a", LiteralizerRecordValue{1}},
        },
    },
    Record0{
        {
            {"b", LiteralizerRecordValue{nullptr}},
        },
    },
};
    (void)my_data;
    return 0;
}
