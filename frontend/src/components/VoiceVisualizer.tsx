import { useEffect, useState } from "react";

interface VoiceVisualizerProps {
  /** Whether to start/stop listening */
  isActive: boolean;
}

const VoiceVisualizer = ({ isActive }: VoiceVisualizerProps) => {
  const [bars, setBars] = useState<number[]>(Array(20).fill(0.2));
  const [volume, setVolume] = useState(0);

  useEffect(() => {
    if (!isActive) {
      setBars(Array(20).fill(0.2));
      setVolume(0);
      return;
    }

    let audioContext: AudioContext | null = null;
    let analyser: AnalyserNode | null = null;
    let source: MediaStreamAudioSourceNode | null = null;
    let rafId: number;

    const handleAudio = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new AudioContext();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 512;

        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);

        const tick = () => {
          analyser!.getByteFrequencyData(dataArray);

          // Calculate average volume between 0 and 1
          let avg = dataArray.reduce((a, b) => a + b, 0) / dataArray.length / 255;

          // 🧩 Noise gate: ignore small ambient noise
          const noiseGate = 0.05; // increase if your environment is noisy
          if (avg < noiseGate) avg = 0;

          // 🎚️ Nonlinear scaling — makes real voice peaks more visible
          const scaled = Math.pow(avg * 1.8, 1.5); // tweak multiplier for intensity
          setVolume(scaled);

          // Animate bars
          const newBars = Array(20)
            .fill(0)
            .map(() => Math.random() * scaled * 2 + 0.05);
          setBars(newBars);

          rafId = requestAnimationFrame(tick);
        };

        tick();
      } catch (err) {
        console.error("🎙️ Microphone access failed:", err);
      }
    };

    handleAudio();

    return () => {
      if (rafId) cancelAnimationFrame(rafId);
      if (source) source.disconnect();
      if (analyser) analyser.disconnect();
      if (audioContext) audioContext.close();
    };
  }, [isActive]);

  return (
    <div className="flex items-center justify-center gap-1 h-24">
      {bars.map((height, i) => (
        <div
          key={i}
          className="w-2 rounded-full bg-gradient-to-t from-primary to-secondary transition-all duration-100"
          style={{
            height: `${Math.min(height, 1) * 100}%`,
            opacity: volume > 0.1 ? 1 : 0.25, // Dim if very quiet
          }}
        />
      ))}
    </div>
  );
};

export default VoiceVisualizer;
