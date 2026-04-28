#include <initializer_list>
#include <string>
#include <map>
auto main() -> int {
auto my_data = std::map<std::string, std::string>{
    {"description", "# not a comment\n"},
    {"name", "foo"},
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"description", "# not a comment\n"},
    {"name", "foo"},
};
    (void)my_data;
    return 0;
}
