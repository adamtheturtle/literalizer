#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    // strings stay data
    "https://example.org/a/*b*/",  // URL annotation
    "escaped quote: \" // still data",
    "backslash: \\",  // outside the string
    "/* not a comment */",
};
    (void)my_data;
    return 0;
}
