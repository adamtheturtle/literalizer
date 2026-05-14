#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    {"message", "no comment here"},
};
    (void)my_data;
    return 0;
}
