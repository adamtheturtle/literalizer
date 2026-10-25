#include <initializer_list>
#include <string>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, int>>{
    {"a", 1},
    {"b", 2},
};
    (void)my_data;
    return 0;
}
