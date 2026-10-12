#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    R"_{}[]#<>%:;.?*(custom base after empty collision: )"
value)_{}[]#<>%:;.?*",
    R"_{}[]#<>%:;.?*(custom suffix after base collision: )" and )x0"
value)_{}[]#<>%:;.?*",
    R"_{}[]#<>%:;.?*(custom second suffix: )" and )x0" and )x00"
value)_{}[]#<>%:;.?*",
    R"_{}[]#<>%:;.?*(long base exhaustion: )" and )abcdefghijklmnop"
value)_{}[]#<>%:;.?*",
};
    (void)my_data;
    return 0;
}
