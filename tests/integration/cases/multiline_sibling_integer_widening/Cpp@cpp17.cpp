#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<long long>>{
    {"a", std::vector<long long>{
        1,
    }},
    {"b", std::vector<long long>{
        1099511627776,
    }},
};
    (void)my_data;
    return 0;
}
