#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector{
    std::map<std::string, double>{{"x", 1}, {"y", 2.5}},
    std::map<std::string, double>{{"x", 3}, {"y", 4.0}},
};
    (void)my_data;
    return 0;
}
