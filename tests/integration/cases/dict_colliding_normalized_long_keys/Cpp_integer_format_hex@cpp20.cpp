#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"a_b", 0x1},
    {"a-b", 0x2},
    {"averyveryverylongkeynamethatgoesonandonandon", 0x3},
    {"averyveryverylongkeynamethatgoesonandmore", 0x4},
};
    (void)my_data;
    return 0;
}
