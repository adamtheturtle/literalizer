#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, int>{
    {"a", 1},  // inline ending backslash \ .
    {"b", 2},
};
    (void)my_data;
    return 0;
}
