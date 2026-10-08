#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"double", "a b"},
    {"single", "c d"},
    {"both", "e f g"},
    {"continued", "hi"},
    {"escaped backslash", "j\\ k"},
};
    (void)my_data;
    return 0;
}
