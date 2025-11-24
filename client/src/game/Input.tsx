import { useRef, useEffect } from "react";
import { InputPacket } from "../types";


export function useInput(send: (input: InputPacket) => void) {
    const seq = useRef(0);
    const state = useRef({
        up: false,
        down: false,
        left: false,
        right: false,
        mouseAngle: 0
    })

    useEffect(() => {
        function handleKey(down: boolean, key: string) {
            if (key === "w" || key === "ArrowUp") state.current.up = down;
            if (key === "s" || key === "ArrowDown") state.current.down = down;
            if (key === "a" || key === "ArrowLeft") state.current.left = down;
            if (key === "d" || key === "ArrowRight") state.current.right = down;
        }

        function onKeyDown(e: KeyboardEvent) { handleKey(true, e.key); }
        function onKeyUp(e: KeyboardEvent) { handleKey(false, e.key); }

        window.addEventListener("keydown", onKeyDown);
        window.addEventListener("keyup", onKeyUp);

        window.addEventListener("mousemove", (e) => {
            state.current.mouseAngle = Math.atan2(
                e.clientY - window.innerHeight / 2,
                e.clientX - window.innerWidth / 2
            );
        });

        const interval = setInterval(() => {
            const packet: InputPacket = {
                seq: seq.current++,
                up: state.current.up,
                down: state.current.down,
                left: state.current.left,
                right: state.current.right,
                mouseAngle: state.current.mouseAngle
            };
            send(packet);
        }, 1000 / 60);

        return () => {
            window.removeEventListener("keydown", onKeyDown);
            window.removeEventListener("keyup", onKeyUp);
            clearInterval(interval);
        }
    }, [send]);
}
