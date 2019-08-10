let handlers = [];

export let Socket = {
    registerHandler: (f) => handlers.push(f),
    socketHandler: (data) => {
            handlers.forEach((f) => {
                f(data);
            })
        },
};
