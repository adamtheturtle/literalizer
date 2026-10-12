#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::string, bool>>{
    1,
    "email",
    true,
};
    (void)my_data;
    return 0;
}
