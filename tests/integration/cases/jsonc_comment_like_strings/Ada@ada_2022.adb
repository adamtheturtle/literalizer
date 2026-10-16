with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AStr ("// data"),
        AStr ("/* data */"),
        AStr ("escaped quote: "" // data"),
        AStr ("backslash: \")
    ];
begin
    null;
end Main;
