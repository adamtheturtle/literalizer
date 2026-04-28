#include <initializer_list>
#include <string>
#include <variant>
int main() {
auto my_data = std::initializer_list<std::variant<bool, int, std::string>>{
    true,
    42,
    "apple",
};
(void)my_data;
my_data = std::initializer_list<std::variant<bool, int, std::string>>{
    true,
    42,
    "apple",
};
    (void)my_data;
    return 0;
}
