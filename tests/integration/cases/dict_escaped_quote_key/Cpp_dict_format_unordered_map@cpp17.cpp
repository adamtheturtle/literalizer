#include <initializer_list>
#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, int>{
    {"a\"b", 1},
};
    (void)my_data;
    return 0;
}
