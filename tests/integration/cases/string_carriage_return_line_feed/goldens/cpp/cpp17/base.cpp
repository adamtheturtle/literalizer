#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"cr", "a\rb"},
    {"crlf", "a\r\nb"},
    {"lf", "a\nb"},
};
    (void)my_data;
    return 0;
}
