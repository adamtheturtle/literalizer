#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::string, bool>>{
    1,
    "hello",
    true,
};
(void)my_data;
my_data = std::vector<std::variant<int, std::string, bool>>{
    1,
    "hello",
    true,
};
    (void)my_data;
    return 0;
}
