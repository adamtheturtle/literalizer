#include <array>
#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::array<std::map<std::string, int>, 1>>{
    {"a", std::array<std::map<std::string, int>, 1>{std::map<std::string, int>{{"k", 1}}}},
    {"b", std::array<std::map<std::string, int>, 1>{std::map<std::string, int>{{"k", 2}}}},
};
    (void)my_data;
    return 0;
}
