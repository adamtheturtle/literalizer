#include <initializer_list>
#include <map>
#include <string>
int main() {
auto my_data = {
    std::map<std::string, std::string>{{"timestamp", "2040-01-01T03:00:00+03:00"}},
    std::map<std::string, std::string>{},
};
    (void)my_data;
    return 0;
}
