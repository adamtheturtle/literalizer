#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::string>>{
    1,
    "email",
    "a@gmail.com",
    100,
};
    (void)my_data;
    return 0;
}
