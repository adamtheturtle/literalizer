#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"within_i32", "2024-01-15T12:00:00"},
    {"beyond_i32", "2099-06-15T08:30:00"},
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"within_i32", "2024-01-15T12:00:00"},
    {"beyond_i32", "2099-06-15T08:30:00"},
};
    (void)my_data;
    return 0;
}
