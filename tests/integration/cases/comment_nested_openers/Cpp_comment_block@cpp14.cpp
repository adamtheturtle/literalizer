#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, int>{
    /* nested openers / * and {- remain */
    {"x", 1},
};
    (void)my_data;
    return 0;
}
