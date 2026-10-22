#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    // heading
    {"count", 2},
};
    (void)my_data;
    return 0;
}
