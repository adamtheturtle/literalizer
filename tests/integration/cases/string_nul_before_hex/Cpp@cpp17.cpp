#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"x", std::string{"before"} + '\0' + "after"},
};
    (void)my_data;
    return 0;
}
