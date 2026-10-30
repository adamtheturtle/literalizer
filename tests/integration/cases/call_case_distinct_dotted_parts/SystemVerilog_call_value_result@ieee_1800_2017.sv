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
class FooType_;
    function _VVal bar(input _VVal x);
        bar = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
    endfunction
endclass
class FooType_;
    FooType_ Foo = new();
endclass
class AType_;
    FooType_ foo = new();
endclass
AType_ a = new();
initial begin
static _VVal my_data = a.foo.Foo.bar(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}"});
end
endmodule
