#include <initializer_list>
#include <string>
#include <map>
int main() {
const auto my_data = std::map<std::string, std::string>{
    {"description", "# not a comment\n"},
    {"name", "foo"},
};
    (void)my_data;
    return 0;
}
