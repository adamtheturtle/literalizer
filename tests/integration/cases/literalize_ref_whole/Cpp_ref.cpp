#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_var = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = my_var;
    (void)my_data;
    return 0;
}
