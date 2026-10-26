#include <array>
#include <map>
#include <string>
int main() {
auto my_data = std::array<std::map<std::string, std::string>, 2>{
    std::map<std::string, std::string>{{"type", "create"}, {"name", "a"}},
    std::map<std::string, std::string>{{"type", "update"}, {"name", "b"}},
};
    (void)my_data;
    return 0;
}
