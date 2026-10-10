#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"explicit_string", "5"},
    {"six", "explicitly tagged key"},
};
    (void)my_data;
    return 0;
}
