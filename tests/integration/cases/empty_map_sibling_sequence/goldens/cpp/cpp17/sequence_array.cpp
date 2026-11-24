#include <initializer_list>
#include <map>
#include <string>
int main() {
auto my_data = {
    std::map<std::string, int>{{"a", 1}},
    std::map<std::string, int>{},
};
    (void)my_data;
    return 0;
}
