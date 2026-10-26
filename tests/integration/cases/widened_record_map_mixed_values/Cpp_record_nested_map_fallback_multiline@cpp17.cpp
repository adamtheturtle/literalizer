#include <vector>
#include <map>
#include <string>
#include <variant>
using LiteralizerRecordValue = std::variant<int, std::string>;
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
            {"b", LiteralizerRecordValue{"two"}},
        },
    },
};
    (void)my_data;
    return 0;
}
