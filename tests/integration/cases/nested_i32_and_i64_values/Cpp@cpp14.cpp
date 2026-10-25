#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<long long>>{
    {"values", std::vector<long long>{1, 2147483648}},
};
    (void)my_data;
    return 0;
}
