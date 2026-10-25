#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, int>>{
    std::map<std::string, int>{{"a-b", 1}},
};
    (void)my_data;
    return 0;
}
