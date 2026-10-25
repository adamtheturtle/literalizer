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
task consume_widget(input _VVal arg_value); endtask
initial begin
static _VVal ref_data[] = '{
    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}
};
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""}
};
void'(consume_widget(my_data));
my_data = ref_data;
void'(consume_widget(my_data));
end
endmodule
