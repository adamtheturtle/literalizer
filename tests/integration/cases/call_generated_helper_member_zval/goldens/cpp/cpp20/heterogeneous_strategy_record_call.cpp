struct objType_ { void ZVal(auto...) const {} };
const objType_ obj;
int main() {
obj.ZVal(1);
    return 0;
}
