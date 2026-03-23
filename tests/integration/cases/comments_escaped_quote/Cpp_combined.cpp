#include <string>
#include <map>
void _check() {
auto my_data = std::map<std::string, std::string>{
    {"key", "value \" # not a comment"},  // real
};
my_data = std::map<std::string, std::string>{
    {"key", "value \" # not a comment"},  // real
};
}
