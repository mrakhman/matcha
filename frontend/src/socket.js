let handlers = [];

export let Socket = {
    registerHandler: (f) => handlers.push(f),
    socketHandler: (data) => {
            console.log(data);
            handlers.forEach((f) => {
                f(data);
            })
        },
};
