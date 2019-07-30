let handlers = [];

export let Socket = {
    registerHandler: (f) => handlers.push(f),
    socketHandler: (data) => {
            // TODO: console
            // console.log(data);
            handlers.forEach((f) => {
                f(data);
            })
        },
};
