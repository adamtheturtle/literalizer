#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
using LiteralizerRecordValue = std::variant<std::string, bool>;
struct Record0 { std::map<std::string, LiteralizerRecordValue> input; std::map<std::string, LiteralizerRecordValue> expected; };
int main() {
auto my_data = std::vector{
    Record0{
        {
            {"kind", LiteralizerRecordValue{"add"}},
            {"item_id", LiteralizerRecordValue{"item_1"}},
            {"urgent", LiteralizerRecordValue{true}},
        },
        {
            {"item_id", LiteralizerRecordValue{"item_1"}},
            {"state", LiteralizerRecordValue{"pending"}},
        },
    },
    Record0{
        {
            {"kind", LiteralizerRecordValue{"remove"}},
            {"item_id", LiteralizerRecordValue{"item_9"}},
        },
        {
            {"error", LiteralizerRecordValue{"not_found"}},
        },
    },
};
    (void)my_data;
    return 0;
}
