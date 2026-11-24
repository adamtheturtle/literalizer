#include <cstddef>
#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::nullptr_t>>{
    {"a", std::vector<std::nullptr_t>{}},
    {"b", std::vector<std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
