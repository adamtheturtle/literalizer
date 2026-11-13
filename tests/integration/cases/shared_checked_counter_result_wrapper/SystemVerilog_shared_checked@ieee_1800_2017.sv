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
module check;
    class Counter;
        int calls = 0;
        function bit accept(_VVal user, _VVal timestamp);
            if (user.s != (calls == 0 ? "user_1" : "user_2") || timestamp.r != 100.0 + calls) $fatal(1, "receiver arguments changed");
            calls++;
            return user.s == "user_1";
        endfunction
    endclass
    int checks = 0;
    function bit checkResult(bit actual, _VVal expected[]);
        if (actual != (expected[0].i != 0) || expected[1].s != (checks == 0 ? "first" : "second")) $fatal(1, "paired result changed");
        checks++;
        return 1;
    endfunction
    initial begin
        static Counter counter = new;
        void'(checkResult(counter.accept(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "user_1"}, _VVal'{tag: _VVAL_REAL, i: 0, r: 100.0, s: ""}), '{_VVal'{tag: _VVAL_BOOL, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "first"}}));
        if (counter.calls != 1 || checks != 1) $fatal(1, "calls skipped");
        $finish;
    end
endmodule
