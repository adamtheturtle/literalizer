#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::string>>{
    std::map<std::string, std::string>{{"type", "create"}, {"name", "a"}},
    std::map<std::string, std::string>{{"type", "update"}, {"name", "b"}},
};
    (void)my_data;
    return 0;
}
