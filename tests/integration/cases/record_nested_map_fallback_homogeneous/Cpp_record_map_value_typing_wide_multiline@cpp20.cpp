#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
using LiteralizerRecordValue = std::string;
struct Record1 { std::string kind; std::string pr_id; };
struct Record0 { std::string name; Record1 input; std::map<std::string, LiteralizerRecordValue> expected; };
int main() {
auto my_data = std::vector{
    Record0{
        .name = "test_1",
        .input = Record1{
            .kind = "create",
            .pr_id = "pr_1",
        },
        .expected = std::map<std::string, LiteralizerRecordValue>{
            {"pr_id", LiteralizerRecordValue{"pr_1"}},
            {"status", LiteralizerRecordValue{"draft"}},
        },
    },
    Record0{
        .name = "test_2",
        .input = Record1{
            .kind = "publish",
            .pr_id = "pr_1",
        },
        .expected = std::map<std::string, LiteralizerRecordValue>{
            {"error", LiteralizerRecordValue{"invalid_operation"}},
        },
    },
};
    (void)my_data;
    return 0;
}
