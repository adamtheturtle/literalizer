#include <array>
#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::array<std::string, 1>>{
    {"a", std::array<std::string, 1>{"x"}},
    {"b", std::array<std::string, 1>{"y"}},
};
    (void)my_data;
    return 0;
}
