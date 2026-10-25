#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"a-b", 1},
    {"two words", 2},
    {"she said \"hi\"", 3},
    {"", 4},
    {"valid_key", 5},
};
    (void)my_data;
    return 0;
}
