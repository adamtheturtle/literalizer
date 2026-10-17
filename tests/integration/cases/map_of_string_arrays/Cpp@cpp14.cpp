#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::string>>{
    {"a", std::vector<std::string>{"x"}},
    {"b", std::vector<std::string>{"y"}},
};
    (void)my_data;
    return 0;
}
