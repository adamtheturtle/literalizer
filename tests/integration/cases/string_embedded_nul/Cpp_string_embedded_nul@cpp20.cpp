#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"x", "\000"},
    {"y", "\0001"},
};
    (void)my_data;
    return 0;
}
