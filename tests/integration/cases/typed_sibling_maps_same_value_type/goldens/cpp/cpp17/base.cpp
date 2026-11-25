#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, int>>{
    std::map<std::string, int>{{"s", 1}},
    std::map<std::string, int>{{"t", 3}},
};
    (void)my_data;
    return 0;
}
