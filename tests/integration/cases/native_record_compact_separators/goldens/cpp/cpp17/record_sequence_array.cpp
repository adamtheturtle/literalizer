#include <vector>
#include <string>
struct Record0 { std::string name; bool active{}; };
int main() {
auto my_data = std::vector{
    Record0{"Ada", true},
};
    (void)my_data;
    return 0;
}
