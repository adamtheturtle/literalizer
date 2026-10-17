#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto existing = 1;
auto my_data = std::map<std::string, std::vector<int>>{
    {"nested", std::vector<int>{0, existing}},
};
    (void)my_data;
    return 0;
}
