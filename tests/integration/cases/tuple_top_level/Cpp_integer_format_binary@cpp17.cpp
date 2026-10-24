#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::string>>{
    0b1,
    "email",
    "a@gmail.com",
    0b1100100,
};
    (void)my_data;
    return 0;
}
