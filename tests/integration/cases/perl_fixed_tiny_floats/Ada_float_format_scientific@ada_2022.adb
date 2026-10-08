with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AFloat (5.0e-324),
        AFloat (-5.0e-324),
        AFloat (2.2250738585072014e-308)
    ];
begin
    null;
end Main;
