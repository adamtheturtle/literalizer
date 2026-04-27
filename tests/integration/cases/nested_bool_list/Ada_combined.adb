with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AList'[ABool (True), ABool (False)],
        AList'[ABool (True), ABool (True)]
    ];
begin
    my_data := AList'[
        AList'[ABool (True), ABool (False)],
        AList'[ABool (True), ABool (True)]
    ];
end Check;
