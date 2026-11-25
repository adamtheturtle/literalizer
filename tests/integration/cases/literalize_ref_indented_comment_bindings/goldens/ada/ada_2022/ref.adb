with A_Stub; use A_Stub;
procedure Main is
            shared : A_Val := AList'[
                AInt (1),
                AInt (2)
            ];
            my_data : A_Val := AList'[
                -- A leading comment with { braces, "quotes", and // markers
                AStr ("first" & Character'Val(10) & "{ ""quoted"" // text }"),
                shared
            ];
begin
    null;
end Main;
