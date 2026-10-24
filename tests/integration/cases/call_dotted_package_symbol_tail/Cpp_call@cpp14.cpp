#include <initializer_list>
#include <vector>
struct helperType_ { template <typename... Args> void list(Args...) const {} };
const helperType_ helper;
int main() {
helper.list(1);
    return 0;
}
