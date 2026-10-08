#include <initializer_list>
#include <vector>
struct helperType_ { void list(auto...) const {} };
const helperType_ helper;
int main() {
helper.list(1);
    return 0;
}
