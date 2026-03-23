#include <initializer_list>
#include <string>
#include <map>
void _check() {
    [[maybe_unused]] _Any _v = std::map<std::string, std::string>{
    {"key", "value \" # not a comment"},  // real
};
}
