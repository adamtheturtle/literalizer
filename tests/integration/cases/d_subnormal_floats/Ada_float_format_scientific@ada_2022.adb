with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AFloat (Long_Float'Value("5.0e-324")),
        AFloat (Long_Float'Value("-5.0e-324")),
        AFloat (Long_Float'Value("1.0e-310"))
    ];
begin
    null;
end Main;
