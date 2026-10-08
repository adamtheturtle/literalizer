#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
using LiteralizerRecordValue = std::variant<int, std::vector<int>>;
struct Record0 { std::string name; std::map<std::string, LiteralizerRecordValue> payload; };
int main() {
auto my_data = std::vector{
    Record0{
        .name = "one",
        .payload = {
            {"scalar", LiteralizerRecordValue{1}},
            {"items", std::vector<int>{
                2,
                3,
            }},
        },
    },
    Record0{
        .name = "two",
        .payload = {
            {"other", LiteralizerRecordValue{2}},
        },
    },
};
    (void)my_data;
    return 0;
}
