#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"description", "# not a comment\n"},
    {"name", "foo"},
};
    (void)my_data;
    return 0;
}
