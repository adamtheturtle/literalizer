#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"starts_at", "09:30:00"},
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"starts_at", "09:30:00"},
};
    (void)my_data;
    return 0;
}
