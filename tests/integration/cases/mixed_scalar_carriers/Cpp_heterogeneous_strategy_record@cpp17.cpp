#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::string, double>>{
    1,
    "a",
    2.5,
};
    (void)my_data;
    return 0;
}
