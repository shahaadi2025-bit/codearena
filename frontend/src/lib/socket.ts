import { io, type Socket } from "socket.io-client";
import { getToken } from "@/lib/api";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:4000";
let socket: Socket | null = null;

// One shared connection per login. A different token (new login) gets a fresh socket.
export function getSocket(): Socket {
  const token = getToken();
  if (!socket || (socket.auth as { token?: string | null }).token !== token) {
    socket?.disconnect();
    socket = io(BASE, { autoConnect: false, auth: { token } });
  }
  return socket;
}

export function disconnectSocket() {
  socket?.disconnect();
  socket = null;
}
