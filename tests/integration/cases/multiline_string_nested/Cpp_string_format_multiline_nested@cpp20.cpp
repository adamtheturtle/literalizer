#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::string>>{
    std::vector<std::string>{R"(first line
  indented

last line)"},
};
    (void)my_data;
    return 0;
}
