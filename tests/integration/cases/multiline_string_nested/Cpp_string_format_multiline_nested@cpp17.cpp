#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<std::string>>>{
    {R"(outer)", std::vector<std::vector<std::string>>{std::vector<std::string>{R"(nested first line
  indented

nested last line
)"}}},
};
    (void)my_data;
    return 0;
}
