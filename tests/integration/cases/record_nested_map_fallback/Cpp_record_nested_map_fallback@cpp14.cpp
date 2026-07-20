#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
using LiteralizerRecordValue = std::variant<std::string, bool>;
struct Record0 { std::string name; std::map<std::string, LiteralizerRecordValue> input; std::map<std::string, LiteralizerRecordValue> expected; };
int main() {
auto my_data = std::vector{
    Record0{.name = "test_1", .input = std::map<std::string, LiteralizerRecordValue>{{"type", LiteralizerRecordValue{"create"}}, {"pr_id", LiteralizerRecordValue{"pr_1"}}, {"draft", LiteralizerRecordValue{true}}}, .expected = std::map<std::string, LiteralizerRecordValue>{{"pr_id", LiteralizerRecordValue{"pr_1"}}, {"status", LiteralizerRecordValue{"draft"}}}},
    Record0{.name = "test_2", .input = std::map<std::string, LiteralizerRecordValue>{{"type", LiteralizerRecordValue{"publish"}}, {"pr_id", LiteralizerRecordValue{"pr_1"}}}, .expected = std::map<std::string, LiteralizerRecordValue>{{"error", LiteralizerRecordValue{"invalid_operation"}}}},
};
    (void)my_data;
    return 0;
}
