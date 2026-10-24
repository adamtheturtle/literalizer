      let shared = [
        1
        2
      ]; in
      let other = 3; in
      let payload = "\n    shared : Val\nshared = RInt 99"; in
      let my_data = {
        a = shared;
        b = other;
        payload = payload;
      }; in my_data
