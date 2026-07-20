#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
};
    (void)my_data;
    return 0;
}
