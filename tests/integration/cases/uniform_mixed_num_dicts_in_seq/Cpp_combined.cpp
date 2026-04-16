#include <initializer_list>
#include <string>
#include <map>
#include <vector>
void check_() {
auto my_data = std::vector<std::map<std::string, double>>{
    std::map<std::string, double>{{"x", 1}, {"y", 2.5}},
    std::map<std::string, double>{{"x", 3}, {"y", 4.0}},
};
my_data = std::vector<std::map<std::string, double>>{
    std::map<std::string, double>{{"x", 1}, {"y", 2.5}},
    std::map<std::string, double>{{"x", 3}, {"y", 4.0}},
};
}
