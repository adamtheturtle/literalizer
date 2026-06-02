#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"user_name", 1},
    {"user.name", 2},
    {"user-name", 3},
    {"field_name_that_is_really_quite_long_one", 4},
    {"field_name_that_is_really_quite_long_two", 5},
};
(void)my_data;
my_data = std::map<std::string, int>{
    {"user_name", 1},
    {"user.name", 2},
    {"user-name", 3},
    {"field_name_that_is_really_quite_long_one", 4},
    {"field_name_that_is_really_quite_long_two", 5},
};
    (void)my_data;
    return 0;
}
