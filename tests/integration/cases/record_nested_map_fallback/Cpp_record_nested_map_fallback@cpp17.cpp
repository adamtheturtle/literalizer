#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <variant>
using LiteralizerRecordValue = std::variant<std::string, bool, std::nullptr_t>;
struct Record0 { std::string name; std::map<std::string, LiteralizerRecordValue> input; std::map<std::string, LiteralizerRecordValue> expected; };
int main() {
auto my_data = std::vector{
    Record0{"test_1", {{"type", LiteralizerRecordValue{"create"}}, {"pr_id", LiteralizerRecordValue{"pr_1"}}, {"draft", LiteralizerRecordValue{true}}, {"missing", LiteralizerRecordValue{nullptr}}}, {{"pr_id", LiteralizerRecordValue{"pr_1"}}, {"status", LiteralizerRecordValue{"draft"}}}},
    Record0{"test_2", {{"type", LiteralizerRecordValue{"publish"}}, {"pr_id", LiteralizerRecordValue{"pr_1"}}}, {{"error", LiteralizerRecordValue{"invalid_operation"}}}},
};
    (void)my_data;
    return 0;
}
