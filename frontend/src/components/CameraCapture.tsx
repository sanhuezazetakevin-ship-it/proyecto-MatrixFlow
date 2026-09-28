import {
  useEffect,
  useRef,
  useState,
} from "react";

interface CameraCaptureProps {
  capturing: boolean;
  totalFrames?: number;
  captureInterval?: number;

  onFramesCaptured: (
    frames: Blob[]
  ) => void;

  onError: (
    message: string
  ) => void;
}

export default function CameraCapture({
  capturing,
  totalFrames = 5,
  captureInterval = 700,
  onFramesCaptured,
  onError,
}: CameraCaptureProps) {

  const videoRef =
    useRef<HTMLVideoElement | null>(null);

  const canvasRef =
    useRef<HTMLCanvasElement | null>(null);

  const streamRef =
    useRef<MediaStream | null>(null);

  const [cameraReady, setCameraReady] =
    useState(false);

  const [capturedCount, setCapturedCount] =
    useState(0);

  // ========================================================
  // INICIAR CÁMARA
  // ========================================================

  useEffect(() => {

    let active = true;

    async function startCamera() {

      try {

        if (
          !navigator.mediaDevices ||
          !navigator.mediaDevices.getUserMedia
        ) {
          throw new Error(
            "Tu navegador no permite utilizar la cámara."
          );
        }

        const stream =
          await navigator.mediaDevices.getUserMedia({
            video: {
              facingMode: "user",
              width: {
                ideal: 640,
              },
              height: {
                ideal: 480,
              },
            },
            audio: false,
          });

        if (!active) {

          stream
            .getTracks()
            .forEach(
              (track) => track.stop()
            );

          return;
        }

        streamRef.current = stream;

        if (videoRef.current) {

          videoRef.current.srcObject =
            stream;

          await videoRef.current.play();

          setCameraReady(true);
        }

      } catch (error) {

        console.error(error);

        onError(
          "No se pudo acceder a la cámara. " +
          "Verifica los permisos del navegador."
        );
      }
    }

    startCamera();

    return () => {

      active = false;

      streamRef.current
        ?.getTracks()
        .forEach(
          (track) => track.stop()
        );

    };

  }, [onError]);

  // ========================================================
  // CAPTURAR FRAMES
  // ========================================================

  useEffect(() => {

    if (!capturing || !cameraReady) {
      return;
    }

    let cancelled = false;

    async function captureSequence() {

      const frames: Blob[] = [];

      setCapturedCount(0);

      for (
        let index = 0;
        index < totalFrames;
        index++
      ) {

        if (cancelled) {
          return;
        }

        if (index > 0) {

          await new Promise<void>(
            (resolve) => {

              window.setTimeout(
                resolve,
                captureInterval
              );

            }
          );
        }

        if (cancelled) {
          return;
        }

        try {

          const frame =
            await captureFrame();

          frames.push(frame);

          setCapturedCount(
            frames.length
          );

        } catch (error) {

          console.error(error);

          onError(
            "No se pudo capturar correctamente la cámara."
          );

          return;
        }
      }

      if (
        !cancelled &&
        frames.length === totalFrames
      ) {

        onFramesCaptured(frames);

      }
    }

    captureSequence();

    return () => {
      cancelled = true;
    };

  }, [
    capturing,
    cameraReady,
    totalFrames,
    captureInterval,
    onFramesCaptured,
    onError,
  ]);

  // ========================================================
  // CAPTURAR UN FRAME
  // ========================================================

  function captureFrame():
  Promise<Blob> {

    return new Promise(
      (resolve, reject) => {

        const video =
          videoRef.current;

        const canvas =
          canvasRef.current;

        if (!video || !canvas) {

          reject(
            new Error(
              "Cámara no disponible."
            )
          );

          return;
        }

        const width =
          video.videoWidth;

        const height =
          video.videoHeight;

        if (
          width === 0 ||
          height === 0
        ) {

          reject(
            new Error(
              "La cámara todavía no está lista."
            )
          );

          return;
        }

        canvas.width = width;
        canvas.height = height;

        const context =
          canvas.getContext("2d");

        if (!context) {

          reject(
            new Error(
              "No se pudo procesar la imagen."
            )
          );

          return;
        }

        /*
         * IMPORTANTE:
         *
         * La vista previa está reflejada con CSS,
         * pero enviamos al backend el frame ORIGINAL.
         *
         * Así evitamos alterar innecesariamente
         * la imagen que procesa InsightFace.
         */

        context.drawImage(
          video,
          0,
          0,
          width,
          height
        );

        canvas.toBlob(
          (blob) => {

            if (!blob) {

              reject(
                new Error(
                  "No se pudo generar la captura."
                )
              );

              return;
            }

            resolve(blob);

          },
          "image/jpeg",
          0.9
        );
      }
    );
  }

  return (
    <div className="camera-component">

      <div className="camera-frame">

        <video
          ref={videoRef}
          className="camera-video"
          autoPlay
          playsInline
          muted
        />

        <div className="face-guide">
          <div className="face-oval" />
        </div>

        {!cameraReady && (
          <div className="camera-overlay">
            Iniciando cámara...
          </div>
        )}

        {capturing && (
          <div className="capture-indicator">

            <span className="capture-dot" />

            Capturando{" "}
            {capturedCount}/{totalFrames}

          </div>
        )}

      </div>

      <canvas
        ref={canvasRef}
        style={{
          display: "none",
        }}
      />

      <p className="camera-help">
        Mantén el rostro visible y centrado
        durante las capturas.
      </p>

    </div>
  );
}