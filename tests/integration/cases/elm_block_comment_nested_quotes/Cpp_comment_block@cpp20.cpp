#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    /* "{-" and '{-' stay readable */
    /* balanced {- nested -} and trailing -} stay readable */
    {"x", 1},
};
    (void)my_data;
    return 0;
}
