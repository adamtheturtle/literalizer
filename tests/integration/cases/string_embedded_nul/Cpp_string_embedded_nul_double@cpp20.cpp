#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"x", std::string{""} + '\0' + ""},
    {"y", std::string{""} + '\0' + "1"},
};
    (void)my_data;
    return 0;
}
