#include <initializer_list>
#include <vector>
#include <string>
#include <map>
int main() {
auto shared = std::vector<int>{
    1,
    2,
};
auto my_data = std::map<std::string, std::vector<int>>{
    {"a", std::move(shared)},
};
(void)my_data;
my_data = std::map<std::string, std::vector<int>>{
    {"a", std::move(shared)},
};
    (void)my_data;
    return 0;
}
