#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::vector<int>>>{
    {"a", std::map<std::string, std::vector<int>>{
        {"b", std::vector<int>{
            1,
            2,
            3,
        }},
    }},
};
    (void)my_data;
    return 0;
}
