#include "../../cpp_support/include/move_only_record.hpp"
#include <utility>
struct Record0 { UserRecord child; };
template <typename... Args> auto consume_widget(Args...) { return 0; }
int main() {
auto first = Record0{
    {
        1,
    },
};
consume_widget(std::move(first));
    return 0;
}
