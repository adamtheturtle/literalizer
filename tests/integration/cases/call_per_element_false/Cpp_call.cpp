#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
void check_() {
process(std::vector<int>{
    1,
});
}
