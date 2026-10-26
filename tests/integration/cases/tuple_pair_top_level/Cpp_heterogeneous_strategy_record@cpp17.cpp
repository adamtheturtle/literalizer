#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, std::string>>{
    1,
    "email",
};
    (void)my_data;
    return 0;
}
