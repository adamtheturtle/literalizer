procedure Check is
   procedure Check_Declaration is
      my_data : A_Val := AInt (9223372036854775808);
   begin
      null;
   end Check_Declaration;
   procedure Check_Assignment is
   begin
      my_data := AInt (9223372036854775808);
   end Check_Assignment;
begin
   null;
end Check;
