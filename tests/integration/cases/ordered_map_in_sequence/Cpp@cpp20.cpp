#include <string>
#include <utility>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::pair<std::string, int>>, std::string>>{
    std::vector<std::pair<std::string, int>>{{"a", 1}},
    "hello",
};
    (void)my_data;
    return 0;
}
