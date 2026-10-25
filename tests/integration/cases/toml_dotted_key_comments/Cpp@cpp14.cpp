#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::map<std::string, int>>{
    // first dotted key
    // second dotted key
    {"a", std::map<std::string, int>{{"b", 1}, {"c", 2}}},
};
    (void)my_data;
    return 0;
}
