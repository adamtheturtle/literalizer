#include <vector>
#include <map>
#include <string>
int main() {
auto shared_values = std::vector<int>{
    1,
    2,
};
auto my_data = std::map<std::string, std::vector<int>>{
    {"a", shared_values},
};
(void)my_data;
my_data = std::map<std::string, std::vector<int>>{
    {"a", shared_values},
};
    (void)my_data;
    return 0;
}
