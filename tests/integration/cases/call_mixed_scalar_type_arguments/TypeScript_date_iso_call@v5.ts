const capture: any = () => {};
capture({ nan_value: NaN, positive_infinity: Infinity, negative_infinity: -Infinity, finite_value: 1.25, date_value: "2024-01-15", datetime_value: new Date(2024, 0, 15, 12, 34, 56), text_value: "[ordinary text]" });
export {};
