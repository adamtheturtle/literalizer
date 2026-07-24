#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::map<std::string, std::vector<std::nullptr_t>>{
    {"a", std::vector<std::nullptr_t>{}},
    {"b", std::vector<std::nullptr_t>{}},
};
(void)my_data;
my_data = std::map<std::string, std::vector<std::nullptr_t>>{
    {"a", std::vector<std::nullptr_t>{}},
    {"b", std::vector<std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
