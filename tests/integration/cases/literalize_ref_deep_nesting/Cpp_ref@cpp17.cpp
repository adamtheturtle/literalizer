#include <initializer_list>
#include <vector>
#include <string>
#include <map>
int main() {
auto deep = std::vector<std::vector<int>>{
    std::vector<int>{
        1,
        2,
    },
    std::vector<int>{
        3,
        4,
    },
};
auto my_data = std::map<std::string, std::map<std::string, std::map<std::string, std::vector<std::vector<int>>>>>{
    {"a", std::map<std::string, std::map<std::string, std::vector<std::vector<int>>>>{
        {"b", std::map<std::string, std::vector<std::vector<int>>>{
            {"c", std::move(deep)},
        }},
    }},
};
    (void)my_data;
    return 0;
}
