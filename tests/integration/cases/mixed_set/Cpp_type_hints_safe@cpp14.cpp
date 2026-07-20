#include <vector>
#include <string>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<bool, int, std::string>>{
    true,
    42,
    "apple",
};
    (void)my_data;
    return 0;
}
