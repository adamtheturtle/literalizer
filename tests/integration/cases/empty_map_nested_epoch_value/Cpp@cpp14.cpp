#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::vector<std::map<std::string, std::map<std::string, std::vector<std::string>>>>{
    std::map<std::string, std::map<std::string, std::vector<std::string>>>{{"nested", std::map<std::string, std::vector<std::string>>{{"times", std::vector<std::string>{"1900-01-01T00:00:00+00:00"}}}}},
    std::map<std::string, std::map<std::string, std::vector<std::string>>>{},
};
    (void)my_data;
    return 0;
}
