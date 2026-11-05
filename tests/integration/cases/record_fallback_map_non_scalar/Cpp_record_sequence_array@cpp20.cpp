#include <vector>
#include <array>
#include <map>
#include <string>
#include <variant>
using LiteralizerRecordValue = std::variant<int, std::array<int, 2>>;
struct Record0 { std::string name; std::map<std::string, LiteralizerRecordValue> payload; };
int main() {
auto my_data = std::vector{
    Record0{.name = "one", .payload = {{"scalar", LiteralizerRecordValue{1}}, {"items", std::array<int, 2>{2, 3}}}},
    Record0{.name = "two", .payload = {{"other", LiteralizerRecordValue{2}}}},
};
    (void)my_data;
    return 0;
}
