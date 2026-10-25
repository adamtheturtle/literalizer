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
task capture(input _VVal nan_value, input _VVal positive_infinity, input _VVal negative_infinity, input _VVal finite_value, input _VVal date_value, input _VVal datetime_value, input _VVal text_value); endtask
initial begin
void'(capture(_VVal'{tag: _VVAL_REAL, i: 0, r: $bitstoreal(64'h7FF8000000000000), s: ""}, _VVal'{tag: _VVAL_REAL, i: 0, r: $bitstoreal(64'h7FF0000000000000), s: ""}, _VVal'{tag: _VVAL_REAL, i: 0, r: $bitstoreal(64'hFFF0000000000000), s: ""}, _VVal'{tag: _VVAL_REAL, i: 0, r: 1.25, s: ""}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-01-15"}, _VVal'{tag: _VVAL_INT, i: 1705322096, r: 0.0, s: ""}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "[ordinary text]"}));
end
endmodule
