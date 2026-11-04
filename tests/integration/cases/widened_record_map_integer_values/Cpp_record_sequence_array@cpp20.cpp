#include <vector>
#include <map>
#include <string>
struct Record0 { std::map<std::string, int> input; };
int main() {
auto my_data = std::vector{
    Record0{.input = {{"a", 1}}},
    Record0{.input = {{"b", 2}}},
};
    (void)my_data;
    return 0;
}
