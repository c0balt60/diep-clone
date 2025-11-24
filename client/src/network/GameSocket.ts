import { InputPacket, PlayerState } from "../types";

const URL = import.meta.env.VITE_SERVER_URL ?? "ws://127.0.0.1:8080/ws";
console.log(URL);
// export const socket = io(URL, { reconnection: true });

export const socket = new WebSocket(URL);

// export function sendInput(input: InputPacket) {
//     socket.emit("input", input);
// }

// export function onInit(data: (payload: { id: string }) => void) {
//     socket.on("init", data);
// }

// export function onState(data: (payload: { players: PlayerState[] }) => void) {
//     socket.on("state", data);
// }

export function sendInput(input: InputPacket) {
    if (socket.readyState !== WebSocket.OPEN) return;
    socket.send(JSON.stringify({ type: "input", input }));
}

export function onInit(data: (payload: { id: string }) => void) {
    // socket.on("init", data);
    socket.addEventListener("message", (event) => {
        const message = JSON.parse(event.data);
        if (message.type === "init") {
            data(message);
        }
    });
}

export function onState(data: (payload: { players: PlayerState[] }) => void) {
    socket.addEventListener("message", (event) => {
        const message = JSON.parse(event.data);
        if (message.type === "state") {
            data(message);
        }
    });
}
