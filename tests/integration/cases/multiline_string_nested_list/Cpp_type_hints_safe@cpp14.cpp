#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::string>>{
    std::vector<std::string>{"\nfirst line\n  indented\n\nlast line\n"},
};
    (void)my_data;
    return 0;
}
