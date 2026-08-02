#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    R"abcdefghijklmnop(custom base after empty collision: )"
value)abcdefghijklmnop",
    R"abcdefghijklmnop(custom suffix after base collision: )" and )x0"
value)abcdefghijklmnop",
    R"abcdefghijklmnop(custom second suffix: )" and )x0" and )x00"
value)abcdefghijklmnop",
    "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue",
};
    (void)my_data;
    return 0;
}
