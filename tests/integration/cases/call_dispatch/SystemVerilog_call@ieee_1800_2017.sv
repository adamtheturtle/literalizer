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
task store_item(input _VVal key, input _VVal value); endtask
task read_item(input _VVal key); endtask
initial begin
store_item(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 10, r: 0.0, s: ""});
read_item(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
end
endmodule
