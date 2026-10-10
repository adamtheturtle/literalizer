#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    R"x0(custom base after empty collision: )"
value)x0",
    R"x00(custom suffix after base collision: )" and )x0"
value)x00",
    R"x01(custom second suffix: )" and )x0" and )x00"
value)x01",
    R"x0(long base exhaustion: )" and )abcdefghijklmnop"
value)x0",
};
    (void)my_data;
    return 0;
}
