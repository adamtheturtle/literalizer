#include <string>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<int>>>{
    {"a", std::vector<int>{1, 2}},
};
    (void)my_data;
    return 0;
}
