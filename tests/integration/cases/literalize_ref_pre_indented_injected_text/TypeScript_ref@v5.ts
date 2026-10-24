      const shared = [
        1,
        2,
      ];
      const other = 3;
      const payload = "\n    shared : Val\nshared = RInt 99";
      const my_data: Record<string, Record<string, string>> = {
        "a": shared,
        "b": other,
        "payload": payload,
      };
export {};
