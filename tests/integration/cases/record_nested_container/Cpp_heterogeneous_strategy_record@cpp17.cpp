#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record0 { std::string title; std::vector<std::string> tags; int priority{}; };
int main() {
auto my_data = Record0{
    "report",
    {
        "draft",
        "urgent",
        "review",
    },
    2,
};
    (void)my_data;
    return 0;
}
