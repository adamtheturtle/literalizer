#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<int>>{
    {"value", std::vector<int>{0, 1}},
};
    (void)my_data;
    return 0;
}
