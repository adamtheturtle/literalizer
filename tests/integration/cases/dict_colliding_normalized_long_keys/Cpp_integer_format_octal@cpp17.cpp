#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"a_b", 01},
    {"a-b", 02},
    {"averyveryverylongkeynamethatgoesonandonandon", 03},
    {"averyveryverylongkeynamethatgoesonandmore", 04},
};
    (void)my_data;
    return 0;
}
