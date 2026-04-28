#include <initializer_list>
#include <string>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::string>{
    "issue #{42}",
    "color #red",
};
(void)my_data;
my_data = std::vector<std::string>{
    "issue #{42}",
    "color #red",
};
    (void)my_data;
    return 0;
}
