#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<std::string>>>{
    {"outer", std::vector<std::vector<std::string>>{std::vector<std::string>{"nested first line\n  indented\n\nnested last line\n"}}},
};
    (void)my_data;
    return 0;
}
