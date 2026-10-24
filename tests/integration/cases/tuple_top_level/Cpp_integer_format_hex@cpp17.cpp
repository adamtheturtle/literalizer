#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::string>>{
    0x1,
    "email",
    "a@gmail.com",
    0x64,
};
    (void)my_data;
    return 0;
}
