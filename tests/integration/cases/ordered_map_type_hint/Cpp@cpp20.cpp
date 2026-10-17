#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<int>>>{
    {"a", std::vector<int>{1, 2}},
};
    (void)my_data;
    return 0;
}
