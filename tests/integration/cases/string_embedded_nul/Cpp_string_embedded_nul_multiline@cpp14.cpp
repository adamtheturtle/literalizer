#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {R"(x)", std::string{""} + '\0' + ""},
    {R"(y)", std::string{""} + '\0' + "1"},
};
    (void)my_data;
    return 0;
}
