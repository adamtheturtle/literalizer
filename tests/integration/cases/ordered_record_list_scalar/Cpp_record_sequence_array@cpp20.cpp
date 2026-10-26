#include <string>
#include <utility>
#include <variant>
#include <vector>
struct Record0 { int id{}; };
int main() {
auto my_data = std::vector<std::pair<std::string, std::variant<std::vector<Record0>, int>>>{
    {"first", std::vector{Record0{.id = 1}}},
    {"second", 2},
};
    (void)my_data;
    return 0;
}
