let handlers = {};

export let Socket = {
    registerHandler: (f, name) => handlers[name] = f,
    unregisterHandler: (name) => {
        if (name in handlers)
            delete handlers[name];
    },
    socketHandler: (data) => {
        Object.keys(handlers).forEach((key) => handlers[key](data));
    }
};
