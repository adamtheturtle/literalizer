#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<double>>{
    std::vector<double>{1},
    std::vector<double>{2.5},
};
    (void)my_data;
    return 0;
}
