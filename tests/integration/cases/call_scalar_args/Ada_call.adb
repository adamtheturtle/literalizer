procedure Check is
      function process (A : Integer) return Integer is (A);
   process(value=>"hello")
   process(value=>42)
   process(value=>ABool (True))
begin
   null;
end Check;
