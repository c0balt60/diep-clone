import React, { useEffect, useRef, useState } from "react";
import { PlayerState } from "../types";
import { onInit, onState, sendInput } from "../network/GameSocket";
import { useInput } from "./Input";

export default function GameCanvas() {
    const cavasRef = React.useRef<HTMLCanvasElement | null>(null);
    const [players, setPlayers] = useState<PlayerState[]>([]);
    const localIdRef = useRef<string | null>(null);

    // Networking handlers
    useEffect(() => {
        onInit((payload) => {
            localIdRef.current = payload.id;
        })
        onState((list) => {
            setPlayers(list.players);
        })
    })

    // Input hook
    useInput((input) => {
        sendInput(input);
    });

    // Canvas update
    useEffect(() => {
        const canvas = cavasRef.current!;
        const canvasContext = canvas?.getContext("2d")!;
        let raf = 0;

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener("resize", resize);

        function draw() {
            canvasContext.clearRect(0, 0, canvas.width, canvas.height);

            // Center player camera
            const local = players.find(player => player.id === localIdRef.current) || { x: 0, y: 0 };
            const localX = local.x;
            const localY = local.y;

            canvasContext.save();

            // Translate local player to center
            canvasContext.translate(canvas.width / 2 - localX, canvas.height / 2 - localY);

            // Draw players
            for (const player of players) {
                canvasContext.save();
                canvasContext.translate(player.x, player.y);
                canvasContext.rotate(player.angle);

                // Draw body
                canvasContext.fillStyle = player.id === localIdRef.current ? "rgb(51, 187, 255)" : "rgba(255, 51, 51, 1)";
                canvasContext.beginPath();
                canvasContext.arc(0, 0, 20, 0, Math.PI * 2);
                canvasContext.fill();

                // barrel
                canvasContext.fillStyle = "grey";
                canvasContext.fillRect(0, -5, 30, 10);

                canvasContext.restore();
            }

            // HUD
            canvasContext.restore();
            raf = requestAnimationFrame(draw);
        }

        raf = requestAnimationFrame(draw);

        return () => {
            window.removeEventListener("resize", resize);
            cancelAnimationFrame(raf);
        }
    }, [players]);

    return <canvas ref={cavasRef} style={{ display: "block", color: "white" }} />;
}
