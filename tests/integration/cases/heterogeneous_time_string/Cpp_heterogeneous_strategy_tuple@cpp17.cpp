#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <tuple>
int main() {
auto my_data = std::map<std::string, std::tuple<std::string, std::string>>{
    {"vals", std::make_tuple("09:30:00", "hello")},
};
    (void)my_data;
    return 0;
}
