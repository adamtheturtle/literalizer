#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"0a", "first"},
    {"1b", "second"},
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"0a", "first"},
    {"1b", "second"},
};
    (void)my_data;
    return 0;
}
