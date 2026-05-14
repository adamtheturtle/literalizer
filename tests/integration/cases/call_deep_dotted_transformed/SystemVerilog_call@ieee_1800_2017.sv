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
class ClientType_;
    function _VVal fetch(input _VVal payload);
        fetch = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
    endfunction
endclass
class AppType_;
    ClientType_ client = new();
endclass
AppType_ app = new();
task emit(input _VVal _arg); endtask
initial begin
emit(app.client.fetch(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hello"}));
emit(app.client.fetch(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}));
emit(app.client.fetch(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}));
end
endmodule
