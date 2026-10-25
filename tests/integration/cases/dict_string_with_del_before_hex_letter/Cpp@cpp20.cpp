#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"value", "deld"},
};
    (void)my_data;
    return 0;
}
