#include <array>
#include <initializer_list>
#include <map>
#include <string>
int main() {
auto my_data = {
    std::map<std::string, std::map<std::string, std::array<std::string, 1>>>{{"nested", std::map<std::string, std::array<std::string, 1>>{{"times", std::array<std::string, 1>{"1900-01-01T00:00:00+00:00"}}}}},
    std::map<std::string, std::map<std::string, std::array<std::string, 1>>>{},
};
    (void)my_data;
    return 0;
}
