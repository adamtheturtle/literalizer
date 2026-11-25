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
    longint expected[6] = '{1, 1, 2, 101, 3, 42};
    if (event_index >= 6 || actual != expected[event_index]) $fatal(1, "receiver event changed");
    event_index++;
endfunction
function automatic _VVal process(_VVal value);
    observe_event(1); observe_event(value.i);
    return _VVal'{tag: _VVAL_INT, i: value.i + 100, r: 0.0, s: ""};
endfunction
function automatic void emit(_VVal actual, _VVal zipped);
    observe_event(2); observe_event(actual.i);
    observe_event(3); observe_event(zipped.i);
endfunction
function automatic void verify_events();
    if (event_index != 6) $fatal(1, "missing receiver events");
    $finish;
endfunction
initial begin
void'(emit(process(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}), _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}));
void'(verify_events());
end
endmodule
