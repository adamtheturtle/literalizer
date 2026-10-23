#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"a_b", 0b1},
    {"a-b", 0b10},
    {"averyveryverylongkeynamethatgoesonandonandon", 0b11},
    {"averyveryverylongkeynamethatgoesonandmore", 0b100},
};
    (void)my_data;
    return 0;
}
