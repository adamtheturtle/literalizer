#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, std::string>>{
    01,
    "email",
    "a@gmail.com",
    0144,
};
    (void)my_data;
    return 0;
}
