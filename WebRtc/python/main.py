from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connections: room_id -> {peer_id -> websocket}
rooms: Dict[str, Dict[str, WebSocket]] = {}

@app.websocket("/ws/{room_id}/{peer_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, peer_id: str):
    await websocket.accept()
    
    # Add to room
    if room_id not in rooms:
        rooms[room_id] = {}
    rooms[room_id][peer_id] = websocket
    
    # Tell new peer who else is in room
    other_peers = [pid for pid in rooms[room_id].keys() if pid != peer_id]
    await websocket.send_json({
        "type": "peers",
        "peers": other_peers
    })
    
    # Tell others about new peer
    for other_id, other_ws in rooms[room_id].items():
        if other_id != peer_id:
            try:
                await other_ws.send_json({
                    "type": "new_peer",
                    "peer_id": peer_id
                })
            except:
                pass
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Forward signaling messages to target peer
            target_id = data.get("target")
            if target_id and target_id in rooms.get(room_id, {}):
                try:
                    await rooms[room_id][target_id].send_json({
                        "type": data["type"],
                        "sender": peer_id,
                        "data": data.get("data")
                    })
                except:
                    pass
                    
    except WebSocketDisconnect:
        # Remove from room
        if room_id in rooms and peer_id in rooms[room_id]:
            del rooms[room_id][peer_id]
            
            # Tell others peer left
            for other_id, other_ws in rooms[room_id].items():
                try:
                    await other_ws.send_json({
                        "type": "peer_left",
                        "peer_id": peer_id
                    })
                except:
                    pass
            
            # Clean empty rooms
            if not rooms[room_id]:
                del rooms[room_id]

@app.get("/")
async def get():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>WebRTC Video Conference</title>
    <style>
        body { font-family: Arial; max-width: 1200px; margin: 50px auto; padding: 20px; }
        #videos { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        video { width: 100%; background: #000; border-radius: 8px; }
        .controls { margin: 20px 0; }
        button { padding: 10px 20px; margin: 5px; cursor: pointer; border: none; border-radius: 5px; font-size: 16px; }
        .join { background: #4CAF50; color: white; }
        .mute { background: #ff9800; color: white; }
        .stop { background: #f44336; color: white; }
        input { padding: 10px; font-size: 16px; margin: 5px; }
    </style>
</head>
<body>
    <h1>WebRTC Video Conference</h1>
    
    <div class="controls">
        <input type="text" id="roomId" placeholder="Room ID" value="room1">
        <button class="join" onclick="joinRoom()">Join Room</button>
        <button class="mute" onclick="toggleMute()">Mute/Unmute</button>
        <button class="mute" onclick="toggleVideo()">Video On/Off</button>
        <button class="stop" onclick="leaveRoom()">Leave</button>
    </div>
    
    <div id="videos">
        <video id="localVideo" autoplay muted playsinline></video>
    </div>

    <script>
        const config = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' },
                { urls: 'stun:stun2.l.google.com:19302' },
                {
                    urls: 'turn:openrelay.metered.ca:80',
                    username: 'openrelayproject',
                    credential: 'openrelayproject'
                },
                {
                    urls: 'turn:openrelay.metered.ca:443',
                    username: 'openrelayproject',
                    credential: 'openrelayproject'
                },
                {
                    urls: 'turn:openrelay.metered.ca:443?transport=tcp',
                    username: 'openrelayproject',
                    credential: 'openrelayproject'
                },
                {
                    urls: 'turn:relay.metered.ca:80',
                    username: 'e9ea4bb4b2acc7b3ec8388bc',
                    credential: 'RYstabilXo+yZcKo'
                },
                {
                    urls: 'turn:relay.metered.ca:443',
                    username: 'e9ea4bb4b2acc7b3ec8388bc',
                    credential: 'RYabilXo+yZcKo'
                }
            ],
            iceCandidatePoolSize: 10,
            iceTransportPolicy: 'all'
        };
        
        let localStream;
        let ws;
        let peers = {};
        const peerId = 'peer_' + Math.random().toString(36).substr(2, 9);
        
        async function joinRoom() {
            const roomId = document.getElementById('roomId').value;
            
            // Get camera + mic
            localStream = await navigator.mediaDevices.getUserMedia({ 
                video: true, 
                audio: true 
            });
            document.getElementById('localVideo').srcObject = localStream;
            
            // Connect to signaling server
            const wsHost = window.location.host;
            const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${wsProtocol}//${wsHost}/ws/${roomId}/${peerId}`);
            
            ws.onmessage = async (event) => {
                const msg = JSON.parse(event.data);
                
                if (msg.type === 'peers') {
                    // Create connections to existing peers
                    for (const pid of msg.peers) {
                        await createPeerConnection(pid, true);
                    }
                } else if (msg.type === 'new_peer') {
                    // New peer joined, wait for their offer
                    await createPeerConnection(msg.peer_id, false);
                } else if (msg.type === 'offer') {
                    await handleOffer(msg.sender, msg.data);
                } else if (msg.type === 'answer') {
                    await handleAnswer(msg.sender, msg.data);
                } else if (msg.type === 'ice') {
                    await handleIce(msg.sender, msg.data);
                } else if (msg.type === 'peer_left') {
                    removePeer(msg.peer_id);
                }
            };
        }
        
        async function createPeerConnection(remotePeerId, createOffer) {
            const pc = new RTCPeerConnection(config);
            peers[remotePeerId] = pc;
            
            console.log(`Creating peer connection with ${remotePeerId}, initiator: ${createOffer}`);
            
            // Add local stream
            localStream.getTracks().forEach(track => {
                pc.addTrack(track, localStream);
                console.log(`Added ${track.kind} track`);
            });
            
            // Handle incoming stream
            pc.ontrack = (event) => {
                console.log(`Received ${event.track.kind} track from ${remotePeerId}`);
                let video = document.getElementById('video_' + remotePeerId);
                if (!video) {
                    video = document.createElement('video');
                    video.id = 'video_' + remotePeerId;
                    video.autoplay = true;
                    video.playsinline = true;
                    document.getElementById('videos').appendChild(video);
                }
                video.srcObject = event.streams[0];
            };
            
            // Handle ICE candidates
            pc.onicecandidate = (event) => {
                if (event.candidate) {
                    console.log(`Sending ICE candidate to ${remotePeerId}`);
                    ws.send(JSON.stringify({
                        type: 'ice',
                        target: remotePeerId,
                        data: event.candidate
                    }));
                }
            };
            
            // Connection state changes
            pc.onconnectionstatechange = () => {
                console.log(`Connection state with ${remotePeerId}: ${pc.connectionState}`);
                if (pc.connectionState === 'failed') {
                    console.log(`Connection failed, attempting restart with ${remotePeerId}`);
                    setTimeout(() => {
                        pc.restartIce();
                    }, 1000);
                }
            };
            
            pc.oniceconnectionstatechange = () => {
                console.log(`ICE connection state with ${remotePeerId}: ${pc.iceConnectionState}`);
                if (pc.iceConnectionState === 'failed') {
                    console.log(`ICE failed, restarting with ${remotePeerId}`);
                    pc.restartIce();
                }
            };
            
            // Create offer if initiator
            if (createOffer) {
                const offer = await pc.createOffer();
                await pc.setLocalDescription(offer);
                console.log(`Sending offer to ${remotePeerId}`);
                ws.send(JSON.stringify({
                    type: 'offer',
                    target: remotePeerId,
                    data: offer
                }));
            }
        }
        
        async function handleOffer(remotePeerId, offer) {
            const pc = peers[remotePeerId];
            console.log(`Received offer from ${remotePeerId}`);
            await pc.setRemoteDescription(offer);
            const answer = await pc.createAnswer();
            await pc.setLocalDescription(answer);
            console.log(`Sending answer to ${remotePeerId}`);
            ws.send(JSON.stringify({
                type: 'answer',
                target: remotePeerId,
                data: answer
            }));
        }
        
        async function handleAnswer(remotePeerId, answer) {
            const pc = peers[remotePeerId];
            console.log(`Received answer from ${remotePeerId}`);
            await pc.setRemoteDescription(answer);
        }
        
        async function handleIce(remotePeerId, candidate) {
            const pc = peers[remotePeerId];
            if (pc && pc.remoteDescription) {
                console.log(`Adding ICE candidate from ${remotePeerId}`);
                await pc.addIceCandidate(candidate);
            } else {
                console.log(`Queuing ICE candidate from ${remotePeerId} (remote desc not ready)`);
            }
        }
        
        function removePeer(remotePeerId) {
            if (peers[remotePeerId]) {
                peers[remotePeerId].close();
                delete peers[remotePeerId];
            }
            const video = document.getElementById('video_' + remotePeerId);
            if (video) video.remove();
        }
        
        function toggleMute() {
            const audioTrack = localStream.getAudioTracks()[0];
            audioTrack.enabled = !audioTrack.enabled;
        }
        
        function toggleVideo() {
            const videoTrack = localStream.getVideoTracks()[0];
            videoTrack.enabled = !videoTrack.enabled;
        }
        
        function leaveRoom() {
            if (ws) ws.close();
            if (localStream) localStream.getTracks().forEach(t => t.stop());
            Object.values(peers).forEach(pc => pc.close());
            location.reload();
        }
    </script>
</body>
</html>
    """)

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
