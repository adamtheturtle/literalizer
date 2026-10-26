#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"comma_hash", "a,#b"},
    {"comma_space_hash", "trail, # comment"},
    {"escaped_quote", "quote \" and , #"},
    {"next_line", "xy"},
    {"line_separator", "x y"},
    {"paragraph_separator", "x y"},
};
    (void)my_data;
    return 0;
}
