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
class FoobarType_;
    task bar(input _VVal x); endtask
endclass
class Foo_BarType_;
    FoobarType_ fooBar = new();
endclass
class AType_;
    Foo_BarType_ foo_bar = new();
endclass
AType_ a = new();
initial begin
void'(a.foo_bar.fooBar.bar(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}"}));
end
endmodule
