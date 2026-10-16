#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "// data",
    "/* data */",
    "escaped quote: \" // data",
    "backslash: \\",
};
    (void)my_data;
    return 0;
}
