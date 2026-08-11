#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"a_b", 1},
    {"a-b", 2},
    {"averyveryverylongkeynamethatgoesonandonandon", 3},
    {"averyveryverylongkeynamethatgoesonandmore", 4},
};
(void)my_data;
my_data = std::map<std::string, int>{
    {"a_b", 1},
    {"a-b", 2},
    {"averyveryverylongkeynamethatgoesonandonandon", 3},
    {"averyveryverylongkeynamethatgoesonandmore", 4},
};
    (void)my_data;
    return 0;
}
