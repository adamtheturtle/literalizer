#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
#include <tuple>
auto process(auto...) { return 0; }
struct tracerType_ { void emit(auto...) const {} };
const tracerType_ tracer;
int main() {
tracer.emit(process("hello"));
tracer.emit(process(42));
tracer.emit(process(true));
    return 0;
}
