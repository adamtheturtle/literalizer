#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<std::string>>>{
    {"mixed", std::vector<std::vector<std::string>>{std::vector<std::string>{"09:30:00"}, std::vector<std::string>{}}},
};
    (void)my_data;
    return 0;
}
