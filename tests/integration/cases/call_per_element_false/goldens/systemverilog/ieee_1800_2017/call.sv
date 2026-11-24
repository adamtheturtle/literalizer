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
int event_index = 0;
function automatic void observe_event(longint actual);
    longint expected[2] = '{1, 1};
    if (event_index >= 2 || actual != expected[event_index]) $fatal(1, "receiver event changed");
    event_index++;
endfunction
function automatic _VVal process(_VVal data);
    observe_event(1); observe_event(data.i);
    return _VVal'{tag: _VVAL_INT, i: data.i + 100, r: 0.0, s: ""};
endfunction
function automatic void verify_events();
    if (event_index != 2) $fatal(1, "missing receiver events");
    $finish;
endfunction
initial begin
void'(process(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}));
void'(verify_events());
end
endmodule
