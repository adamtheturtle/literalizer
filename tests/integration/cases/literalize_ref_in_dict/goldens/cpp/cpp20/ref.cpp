#include <map>
#include <string>
int main() {
auto my_var = 1;
auto my_data = std::map<std::string, int>{
    {"key", my_var},
};
    (void)my_data;
    return 0;
}
