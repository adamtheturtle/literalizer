#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"key", "it's here"},  // a comment
};
(void)my_data;
my_data = std::map<std::string, std::string>{
    {"key", "it's here"},  // a comment
};
    (void)my_data;
    return 0;
}
