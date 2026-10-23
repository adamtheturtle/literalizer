#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"a", 0x1},
    {"b", 0x10000000000},
};
    (void)my_data;
    return 0;
}
