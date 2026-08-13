#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, double>{
    {"pi", 3.141592653589793},
};
    (void)my_data;
    return 0;
}
