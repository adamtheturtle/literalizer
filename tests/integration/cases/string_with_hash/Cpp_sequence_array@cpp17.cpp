#include <array>
#include <string>
int main() {
auto my_data = std::array<std::string, 2>{
    "issue #{42}",
    "color #red",
};
    (void)my_data;
    return 0;
}
