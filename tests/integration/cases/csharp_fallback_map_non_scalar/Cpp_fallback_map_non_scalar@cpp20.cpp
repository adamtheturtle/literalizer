#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct Record0 { std::string name; std::map<std::string, int> payload; };
int main() {
auto my_data = std::vector{
    Record0{.name = "one", .payload = {{"scalar", 1}, {"items", std::vector<int>{2, 3}}}},
    Record0{.name = "two", .payload = {{"other", 2}}},
};
    (void)my_data;
    return 0;
}
