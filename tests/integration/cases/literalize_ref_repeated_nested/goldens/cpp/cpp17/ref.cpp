#include <vector>
#include <map>
#include <string>
int main() {
auto shared = std::vector<int>{
    1,
    2,
};
auto my_data = std::vector<std::map<std::string, std::vector<int>>>{
    std::map<std::string, std::vector<int>>{{"left", shared}, {"right", shared}},
};
    (void)my_data;
    return 0;
}
