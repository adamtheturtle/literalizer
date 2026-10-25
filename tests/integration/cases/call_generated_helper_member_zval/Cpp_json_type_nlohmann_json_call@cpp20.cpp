#include <nlohmann/json.hpp>
struct objType_ { void ZVal(auto...) const {} };
const objType_ obj;
int main() {
    try {
obj.ZVal(nlohmann::json(1));
        return 0;
    } catch (...) {
        return 1;
    }
}
