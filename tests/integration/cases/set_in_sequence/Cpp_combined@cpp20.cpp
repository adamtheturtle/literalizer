#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::initializer_list<std::string>>{
    std::initializer_list<std::string>{"a", "b"},
};
(void)my_data;
my_data = std::vector<std::initializer_list<std::string>>{
    std::initializer_list<std::string>{"a", "b"},
};
    (void)my_data;
    return 0;
}
