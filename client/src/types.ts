export type ID = string;

export interface PlayerState {
    id: ID;
    x: number;
    y: number;
    angle: number;
    health: number;
    score: number;
}

export interface InputPacket {
    seq: number;
    up: boolean;
    down: boolean;
    left: boolean;
    right: boolean;
    mouseAngle: number;
}
