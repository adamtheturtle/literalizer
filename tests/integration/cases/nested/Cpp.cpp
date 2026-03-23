#include <initializer_list>
#include <string>
#include <map>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    {"users", {{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, {{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
}
