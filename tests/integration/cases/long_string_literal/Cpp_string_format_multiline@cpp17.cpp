#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {R"(long_str)", R"(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)"},
    {R"(quoted)", R"(a"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"b)"},
    {R"(wide)", R"(中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中)"},
};
    (void)my_data;
    return 0;
}
