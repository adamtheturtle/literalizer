#include <initializer_list>
#include <string>
#include <map>
void check_() {
auto my_data = std::map<std::string, std::string>{
    {"description", "# not a comment\n"},
    {"name", "foo"},
};
}
