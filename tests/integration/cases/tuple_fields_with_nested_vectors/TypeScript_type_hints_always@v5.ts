const my_data: Record<string, (number | unknown[])[] | (number | string[])[]> = {
  "lint": [2, []],
  "test": [5, ["compile"]],
  "package": [7, ["link", "test"]],
};
export {};
