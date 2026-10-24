#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::vector<std::map<std::string, int>>{
    std::map<std::string, int>{{"a", 1}},
    std::map<std::string, int>{},
};
    (void)my_data;
    return 0;
}
