#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::string>>{
    std::map<std::string, std::string>{{"", "external_value"}},
};
    (void)my_data;
    return 0;
}
