#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::vector<std::map<std::string, std::vector<int>>>{
    std::map<std::string, std::vector<int>>{{"value", std::vector<int>{}}},
    std::map<std::string, std::vector<int>>{{"value", std::vector<int>{1}}},
};
(void)my_data;
my_data = std::vector<std::map<std::string, std::vector<int>>>{
    std::map<std::string, std::vector<int>>{{"value", std::vector<int>{}}},
    std::map<std::string, std::vector<int>>{{"value", std::vector<int>{1}}},
};
    (void)my_data;
    return 0;
}
