#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, int>>{
    std::map<std::string, int>{},
    std::map<std::string, int>{{"value", 1}},
};
    (void)my_data;
    return 0;
}
