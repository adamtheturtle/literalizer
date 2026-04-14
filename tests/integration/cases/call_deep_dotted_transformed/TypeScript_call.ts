declare const app: any;
declare const emit: any;
emit(app.client.fetch({ payload: "hello" }));
emit(app.client.fetch({ payload: 42 }));
emit(app.client.fetch({ payload: true }));
export {};
