#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, int>{
    {"quote\"backslash\\", 1},
    {"line\nbreak", 2},
    {"$(literal)${text}", 3},
    {"RStr prefix", 4},
};
    (void)my_data;
    return 0;
}
