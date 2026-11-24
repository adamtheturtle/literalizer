#include <string>
#include <variant>
#include <vector>
int main() {
auto shared = std::vector<std::variant<int, std::string>>{
    1,
    "x",
};
auto my_data = std::vector<std::vector<std::variant<int, std::string>>>{
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
