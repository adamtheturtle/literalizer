#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct Record1 { std::string kind; std::string pr_id; };
struct Record0 { std::string name; Record1 input; std::map<std::string, std::string> expected; };
int main() {
auto my_data = std::vector{
    Record0{
        "test_1",
        {
            "create",
            "pr_1",
        },
        {
            {"pr_id", "pr_1"},
            {"status", "draft"},
        },
    },
    Record0{
        "test_2",
        {
            "publish",
            "pr_1",
        },
        {
            {"error", "invalid_operation"},
        },
    },
};
    (void)my_data;
    return 0;
}
