#include <initializer_list>
#include <string>
#include <vector>
#include <map>
auto process(auto...) { return 0; }
int main() {
auto big_list = std::vector<std::string>{
    "x",
};
process(std::map<std::string, std::vector<std::string>>{{"k", big_list}}, std::vector<std::pair<std::string, std::map<std::string, std::string>>>{{"m", big_list}});
    return 0;
}
