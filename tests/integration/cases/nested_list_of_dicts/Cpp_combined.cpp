#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<std::vector<std::map<std::string, std::string>>>{
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "Alice"}}, std::map<std::string, std::string>{{"name", "Bob"}}},
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "Charlie"}}, std::map<std::string, std::string>{{"name", "Dave"}}},
};
my_data = std::vector<std::vector<std::map<std::string, std::string>>>{
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "Alice"}}, std::map<std::string, std::string>{{"name", "Bob"}}},
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "Charlie"}}, std::map<std::string, std::string>{{"name", "Dave"}}},
};
}
