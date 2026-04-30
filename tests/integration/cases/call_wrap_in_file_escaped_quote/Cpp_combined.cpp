#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::string>>{
    std::vector<std::string>{"a\"b"},
};
(void)my_data;
my_data = std::vector<std::vector<std::string>>{
    std::vector<std::string>{"a\"b"},
};
    (void)my_data;
    return 0;
}
