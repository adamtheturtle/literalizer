#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<long long>>{
    {"a", std::vector<long long>{4294967296, 4294967297}},
};
    (void)my_data;
    return 0;
}
