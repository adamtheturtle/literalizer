#include <map>
#include <string>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<std::map<std::string, int>>>>{
    {"rows", std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"replacement", -1}, {"present", 1}}, std::map<std::string, int>{{"replacement", 2}, {"present", 3}}}},
};
    (void)my_data;
    return 0;
}
