#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "custom base after empty collision: )\"\nvalue",
    "custom suffix after base collision: )\" and )x0\"\nvalue",
    "custom second suffix: )\" and )x0\" and )x00\"\nvalue",
    "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue",
};
    (void)my_data;
    return 0;
}
