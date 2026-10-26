#include <map>
#include <string>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<std::map<std::string, int>>>>{
    {"entries", std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"id", 1}}}},
};
    (void)my_data;
    return 0;
}
