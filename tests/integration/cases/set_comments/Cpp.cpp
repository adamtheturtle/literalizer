#include <initializer_list>
#include <string>
int main() {
auto my_data = std::initializer_list<std::string>{
    "apple",  // inline comment
    // before banana
    "banana",
    // trailing
};
    (void)my_data;
    return 0;
}
