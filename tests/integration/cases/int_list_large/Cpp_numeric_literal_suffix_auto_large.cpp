#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<long>{
    1000000L,
    -1234L,
    255L,
    -10L,
};
    (void)my_data;
    return 0;
}
