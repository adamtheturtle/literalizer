#include <string>
#include <map>
void _check() {
auto my_data = std::map<std::string, std::string>{
    {"key\nwith\nnewlines", "value1"},
    {"key\twith\ttabs", "value2"},
    {"", "value3"},
};
}
