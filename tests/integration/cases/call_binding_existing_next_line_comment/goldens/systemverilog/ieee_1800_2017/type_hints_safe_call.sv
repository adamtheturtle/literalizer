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
    longint expected[6] = '{2, 42, 1, 42, 2, 142};
    if (event_index >= 6 || actual != expected[event_index]) $fatal(1, "receiver event changed");
    event_index++;
endfunction
function automatic _VVal make_widget(_VVal count);
    observe_event(1); observe_event(count.i);
    return _VVal'{tag: _VVAL_INT, i: count.i + 100, r: 0.0, s: ""};
endfunction
function automatic void consume_widget(_VVal count);
    observe_event(2); observe_event(count.i);
endfunction
function automatic void verify_events();
    if (event_index != 6) $fatal(1, "missing receiver events");
    $finish;
endfunction
initial begin
static _VVal my_data = _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""};
void'(consume_widget(my_data));
my_data = make_widget(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""});
// note
void'(consume_widget(my_data));
void'(verify_events());
end
endmodule
