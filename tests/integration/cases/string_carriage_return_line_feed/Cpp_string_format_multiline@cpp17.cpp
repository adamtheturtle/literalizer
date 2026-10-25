#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {R"(cr)", "a\rb"},
    {R"(crlf)", "a\r\nb"},
    {R"(lf)", R"(a
b)"},
};
    (void)my_data;
    return 0;
}
