import { useState, useEffect, useRef, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";

const WS_URL = "ws://127.0.0.1:8000/ws/";

// Helper to convert audio blob to base64
const blobToBase64 = (blob: Blob): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      if (reader.result) {
        // result is "data:audio/webm;base64,..."
        // We only want the base64 part
        const base64 = (reader.result as string).split(",")[1];
        resolve(base64);
      } else {
        reject("Failed to convert blob to base64");
      }
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
};


export const useVoiceSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [isListening, setIsListening] = useState(false);
  const socket = useRef<WebSocket | null>(null);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const client_id = useRef<string>(uuidv4());
  const audioContext = useRef<AudioContext | null>(null);
  const processor = useRef<ScriptProcessorNode | null>(null);
  const source = useRef<MediaStreamAudioSourceNode | null>(null);

  const connectSocket = useCallback(() => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      console.log("WebSocket is already connected.");
      return;
    }

    console.log(`Connecting to WebSocket with client ID: ${client_id.current}`);
    socket.current = new WebSocket(`${WS_URL}${client_id.current}`);
    socket.current.binaryType = "arraybuffer";

    socket.current.onopen = () => {
      setIsConnected(true);
      console.log("WebSocket connected");
    };

    socket.current.onclose = (event) => {
      setIsConnected(false);
      console.log("WebSocket disconnected:", event.reason);
    };

    socket.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    }

    socket.current.onmessage = (event) => {
        if (typeof event.data === 'string') {
            try {
              const message = JSON.parse(event.data);
              if (message.text) {
                  console.log("Received transcript:", message.text);
                  setTranscript(message.text);
              }
            } catch (e) {
              console.error("Failed to parse JSON message:", event.data);
            }
        } else if (event.data instanceof Blob) {
            // Handle audio stream from server
            const audioBlob = new Blob([event.data], { type: 'audio/mpeg' });
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play().catch(e => console.error("Audio play failed:", e));
        }
    };
  }, []);

  const disconnectSocket = () => {
    if (socket.current) {
      socket.current.close();
      socket.current = null;
    }
    stopListening();
  }

  const startListening = useCallback(async () => {
    if (!socket.current || socket.current.readyState !== WebSocket.OPEN) {
      console.log("Socket not connected. Please connect first.");
      // Attempt to connect, and wait a moment before proceeding.
      connectSocket();
      await new Promise(resolve => setTimeout(resolve, 1000));
      if (!socket.current || socket.current.readyState !== WebSocket.OPEN) {
        console.error("Failed to establish WebSocket connection.");
        return;
      }
    }

    if (isListening) {
      console.log("Already listening.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const AudioContext = window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioContext) {
        console.error("Browser does not support Web Audio API");
        return;
      }
      audioContext.current = new AudioContext();
      source.current = audioContext.current.createMediaStreamSource(stream);
      processor.current = audioContext.current.createScriptProcessor(4096, 1, 1);

      processor.current.onaudioprocess = (e) => {
        if (!isListening || !socket.current || socket.current.readyState !== WebSocket.OPEN) {
          return;
        }
        const inputData = e.inputBuffer.getChannelData(0);
        const pcmData = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
            pcmData[i] = inputData[i] * 32767;
        }
        socket.current.send(pcmData.buffer);
      };

      source.current.connect(processor.current);
      // processor.current.connect(audioContext.current.destination); // Removed to prevent audio feedback
      setIsListening(true);
      console.log("Started listening");

    } catch (error) {
      console.error("Error starting listening:", error);
    }
  }, [isListening, connectSocket]);

  const stopListening = useCallback(() => {
    if (!isListening) return;

    setIsListening(false);
    if (source.current) {
      source.current.disconnect();
      source.current = null;
    }
    if (processor.current) {
      processor.current.disconnect();
      processor.current = null;
    }
    if (audioContext.current) {
      audioContext.current.close();
      audioContext.current = null;
    }
    console.log("Stopped listening");
  }, [isListening]);


  useEffect(() => {
    // Cleanup on unmount
    return () => {
      disconnectSocket();
    };
  }, []);


  const sendText = (text: string) => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      console.log("Sending text:", text);
      socket.current.send(JSON.stringify({ text }));
    } else {
      console.error("Cannot send text, WebSocket is not connected.");
    }
  };

  return {
    isConnected,
    transcript,
    isListening,
    startListening,
    stopListening,
    sendText,
    connectSocket,
  };
};

