import { useCallback, useEffect, useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";

const WS_URL = "ws://127.0.0.1:8000/ws/";

export const useVoiceSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [isListening, setIsListening] = useState(false);
  const isListeningRef = useRef(false);

  const socket = useRef<WebSocket | null>(null);
  const client_id = useRef<string>(uuidv4());

  const audioContext = useRef<AudioContext | null>(null);
  const source = useRef<MediaStreamAudioSourceNode | null>(null);
  const processor = useRef<AudioWorkletNode | ScriptProcessorNode | null>(null);

  const audioQueue = useRef<Uint8Array[]>([]);
  const audioElement = useRef<HTMLAudioElement | null>(null);
  const receivingAudio = useRef<boolean>(false);

  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string; timestamp: string }[]
  >([]);

  // --- Audio playback helper ---
  const playAudioChunks = useCallback(async (chunks: Uint8Array[]) => {
    if (chunks.length === 0) return;
    console.log(`🔊 Playing ${chunks.length} audio chunks combined`);

    const audioBlob = new Blob(chunks, { type: "audio/mpeg" });
    const audioUrl = URL.createObjectURL(audioBlob);

    if (audioElement.current) {
      audioElement.current.pause();
      audioElement.current = null;
    }

    const audio = new Audio(audioUrl);
    audioElement.current = audio;

    return new Promise<void>((resolve) => {
      audio.onended = () => {
        console.log("🔊 Audio playback completed");
        URL.revokeObjectURL(audioUrl);
        audioElement.current = null;
        resolve();
      };
      audio.onerror = (e) => {
        console.error("Audio play failed:", e);
        URL.revokeObjectURL(audioUrl);
        resolve();
      };
      audio.play().catch((e) => {
        console.error("Audio play failed:", e);
        URL.revokeObjectURL(audioUrl);
        resolve();
      });
    });
  }, []);

  // --- WebSocket connection ---
  const connectSocket = useCallback(() => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      console.log("WebSocket already connected");
      return;
    }

    console.log(`Connecting WebSocket → ${client_id.current}`);
    socket.current = new WebSocket(`${WS_URL}${client_id.current}`);
    socket.current.binaryType = "arraybuffer";

    socket.current.onopen = () => {
      setIsConnected(true);
      console.log("✅ WebSocket connected");
    };

    socket.current.onclose = (e) => {
      setIsConnected(false);
      console.log("❌ WebSocket disconnected:", e.reason);
    };

    socket.current.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    socket.current.onmessage = (event) => {
      if (typeof event.data === "string") {
        try {
          const message = JSON.parse(event.data);
          if (message.text) setTranscript(message.text);

          if (message.is_final || message.isFinal) {
            const role: "user" | "assistant" =
              message.role === "user" ? "user" : "assistant";
            setMessages((prev) => [
              ...prev,
              {
                role,
                content: message.text,
                timestamp: new Date().toLocaleTimeString(),
              },
            ]);

            if (role === "assistant") {
              receivingAudio.current = false;
              if (audioQueue.current.length > 0) {
                const chunks = [...audioQueue.current];
                audioQueue.current = [];
                playAudioChunks(chunks);
              }
            }
          }
        } catch (err) {
          console.error("Failed to parse JSON:", event.data);
        }
      } else if (event.data instanceof ArrayBuffer) {
        console.log("📥 Received audio chunk:", event.data.byteLength, "bytes");
        receivingAudio.current = true;
        audioQueue.current.push(new Uint8Array(event.data));
      }
    };
  }, [playAudioChunks]);

  const disconnectSocket = useCallback(() => {
    if (socket.current) {
      socket.current.close();
      socket.current = null;
    }
    if (audioElement.current) {
      audioElement.current.pause();
      audioElement.current = null;
    }
    audioQueue.current = [];
    stopListening();
  }, []);

  // --- Audio capture setup ---
  const startListening = useCallback(async () => {
    if (!socket.current || socket.current.readyState !== WebSocket.OPEN) {
      connectSocket();
      await new Promise((r) => setTimeout(r, 800));
    }

    if (isListeningRef.current) {
      console.log("Already listening");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      const AudioContextClass =
        window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioContextClass) {
        console.error("Browser does not support Web Audio API");
        return;
      }

      audioContext.current = new AudioContextClass({ sampleRate: 16000 });
      source.current = audioContext.current.createMediaStreamSource(stream);

      // --- Try to use AudioWorklet for efficiency ---
      try {
        await audioContext.current.audioWorklet.addModule(
          URL.createObjectURL(
            new Blob(
              [
                `
                class PCMProcessor extends AudioWorkletProcessor {
                  process(inputs) {
                    const input = inputs[0][0];
                    if (!input) return true;
                    const pcm = new Int16Array(input.length);
                    for (let i = 0; i < input.length; i++) {
                      pcm[i] = input[i] * 32767;
                    }
                    this.port.postMessage(pcm.buffer);
                    return true;
                  }
                }
                registerProcessor('pcm-processor', PCMProcessor);
              `,
              ],
              { type: "application/javascript" }
            )
          )
        );

        processor.current = new AudioWorkletNode(
          audioContext.current,
          "pcm-processor"
        );

        processor.current.port.onmessage = (e) => {
          if (
            isListeningRef.current &&
            socket.current &&
            socket.current.readyState === WebSocket.OPEN
          ) {
            socket.current.send(e.data);
          }
        };

        source.current.connect(processor.current);
        // ✅ No connection to destination → muted, efficient
      } catch (err) {
        console.warn("AudioWorklet not supported, using ScriptProcessor fallback", err);

        const scriptNode = audioContext.current.createScriptProcessor(4096, 1, 1);
        scriptNode.onaudioprocess = (e) => {
          if (
            !isListeningRef.current ||
            !socket.current ||
            socket.current.readyState !== WebSocket.OPEN
          )
            return;

          const input = e.inputBuffer.getChannelData(0);
          const pcm = new Int16Array(input.length);
          for (let i = 0; i < input.length; i++) pcm[i] = input[i] * 32767;
          socket.current.send(pcm.buffer);
        };
        source.current.connect(scriptNode);
        processor.current = scriptNode;
      }

      setIsListening(true);
      isListeningRef.current = true;
      console.log("🎙️ Listening started");
    } catch (error) {
      console.error("Error starting mic:", error);
    }
  }, [connectSocket]);

  const stopListening = useCallback(() => {
    if (!isListeningRef.current) return;

    isListeningRef.current = false;
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

    console.log("🛑 Listening stopped");
  }, []);

  // --- Cleanup ---
  useEffect(() => {
    return () => {
      disconnectSocket();
    };
  }, [disconnectSocket]);

  const sendText = (text: string) => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      socket.current.send(JSON.stringify({ text }));
      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          content: text,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    }
  };

  return {
    isConnected,
    transcript,
    messages,
    isListening,
    startListening,
    stopListening,
    sendText,
    connectSocket,
  };
};
