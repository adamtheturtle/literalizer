const make_widget: any = () => {};
make_widget({ before: [] as const, populated: [1] as const, after: [] as const });
make_widget({ before: ["text"] as const, populated: [2] as const, after: [] as const });
make_widget({ before: [] as const, populated: ["text"] as const, after: [] as const });
make_widget({ before: ["text"] as const, populated: [2] as const, after: [3] as const });
export {};
