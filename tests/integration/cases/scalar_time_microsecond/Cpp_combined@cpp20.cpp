#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"exact_millisecond", "09:30:15.123000"},
    {"sub_millisecond", "09:30:15.123456"},
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"exact_millisecond", "09:30:15.123000"},
    {"sub_millisecond", "09:30:15.123456"},
};
    (void)my_data;
    return 0;
}
