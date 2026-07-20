#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::string, int>>{
    "hello",
    42,
};
(void)my_data;
my_data = std::vector<std::variant<std::string, int>>{
    "hello",
    42,
};
    (void)my_data;
    return 0;
}
