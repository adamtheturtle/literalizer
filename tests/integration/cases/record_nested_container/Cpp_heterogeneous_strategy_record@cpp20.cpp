#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record0 { std::string title; std::vector<std::string> tags; int priority{}; };
int main() {
auto my_data = Record0{
    .title = "report",
    .tags = {
        "draft",
        "urgent",
        "review",
    },
    .priority = 2,
};
    (void)my_data;
    return 0;
}
