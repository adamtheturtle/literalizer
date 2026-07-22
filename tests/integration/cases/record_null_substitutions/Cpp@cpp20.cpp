#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <utility>
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<std::map<std::string, int>>>>{
    {"rows", std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"replacement", -1}, {"present", 1}}, std::map<std::string, int>{{"replacement", 2}, {"present", 3}}}},
};
    (void)my_data;
    return 0;
}
