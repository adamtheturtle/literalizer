struct objType_ { void BEGIN(auto...) const {} };
const objType_ obj;
int main() {
obj.BEGIN(42);
    return 0;
}
