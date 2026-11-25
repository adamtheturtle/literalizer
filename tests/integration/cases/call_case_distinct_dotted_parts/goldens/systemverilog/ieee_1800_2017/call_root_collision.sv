typedef enum int {_VVAL_BOOL, _VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
typedef struct {
    string k;
    _VVal v;
} _VKV;
module main;
class FooType_1;
    task bar(input _VVal x); endtask
endclass
class FooType_0;
    FooType_1 Foo = new();
endclass
FooType_0 foo = new();
initial begin
void'(foo.Foo.bar(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}"}));
end
endmodule
