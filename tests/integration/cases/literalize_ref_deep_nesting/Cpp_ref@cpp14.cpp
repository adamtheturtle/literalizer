#include <initializer_list>
#include <string>
#include <vector>
#include <map>
int main() {
auto deep = std::vector<std::vector<std::string>>{
    std::vector<std::string>{
        "one",
        "two",
    },
    std::vector<std::string>{
        "three",
        "four",
    },
};
auto my_data = std::map<std::string, std::map<std::string, std::map<std::string, std::vector<std::vector<std::string>>>>>{
    {"a", std::map<std::string, std::map<std::string, std::vector<std::vector<std::string>>>>{
        {"b", std::map<std::string, std::vector<std::vector<std::string>>>{
            {"c", std::move(deep)},
        }},
    }},
};
    (void)my_data;
    return 0;
}
