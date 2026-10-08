#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"a-b", 1},
    {"a-b-2", 2},
    {"a b", 3},
};
    (void)my_data;
    return 0;
}
