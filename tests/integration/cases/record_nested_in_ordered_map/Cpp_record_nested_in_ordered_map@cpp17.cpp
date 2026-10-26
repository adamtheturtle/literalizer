#include <string>
#include <utility>
#include <vector>
#include <cstddef>
struct Record0 { std::nullptr_t name{}; int id{}; };
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<Record0>>>{
    {"outer", std::vector{Record0{nullptr, 1}}},
};
    (void)my_data;
    return 0;
}
