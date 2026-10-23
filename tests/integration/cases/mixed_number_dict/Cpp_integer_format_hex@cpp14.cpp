#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, double>{
    {"a", 0x1},
    {"b", 2.5},
    {"c", 0x3},
};
    (void)my_data;
    return 0;
}
