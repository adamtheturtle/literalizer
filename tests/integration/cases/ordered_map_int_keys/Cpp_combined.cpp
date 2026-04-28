#include <initializer_list>
#include <string>
#include <utility>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::pair<std::string, std::string>>{
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
(void)my_data;
my_data = std::vector<std::pair<std::string, std::string>>{
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
    (void)my_data;
    return 0;
}
