#include <initializer_list>
#include <string>
#include <map>
void _check() {
    [[maybe_unused]] _Any _v = std::map<std::string, std::string>{
    {"key\nwith\nnewlines", "value1"},
    {"key\twith\ttabs", "value2"},
    {"", "value3"},
};
}
