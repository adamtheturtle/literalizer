const capture: any = () => {};
capture({ nan_value: NaN, positive_infinity: Infinity, negative_infinity: -Infinity, finite_value: 1.25, date_value: new Date(2024, 0, 15), datetime_value: 1705322096, text_value: "[ordinary text]" });
export {};
