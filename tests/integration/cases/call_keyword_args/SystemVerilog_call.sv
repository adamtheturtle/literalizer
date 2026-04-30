typedef enum int {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
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
class ThrottlerType_;
    function _VVal check(input _VVal user_id, input _VVal ts);
        check = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
    endfunction
endclass
ThrottlerType_ throttler = new();
task emit(input _VVal _arg); endtask
initial begin
emit(throttler.check(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "user_1"}, _VVal'{tag: _VVAL_REAL, i: 0, r: 1000.0, s: ""}));
emit(throttler.check(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "user_2"}, _VVal'{tag: _VVAL_REAL, i: 0, r: 2000.5, s: ""}));
end
endmodule
