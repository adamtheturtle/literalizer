#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::map<std::string, std::vector<int>>{
    {"a", std::vector<int>{1, 2}},
    {"b", std::vector<int>{}},
};
    (void)my_data;
    return 0;
}
