#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"morning", "09:30:00"},
    {"afternoon", "14:15:00"},
    {"evening", "23:59:59"},
};
    (void)my_data;
    return 0;
}
