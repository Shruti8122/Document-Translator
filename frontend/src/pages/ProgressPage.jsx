import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  FiUploadCloud,
  FiFileText,
  FiCpu,
  FiGlobe,
  FiCheckCircle,
  FiLoader,
  FiAlertCircle,
} from "react-icons/fi";

import GlassCard from "../components/GlassCard";
import { getProgress } from "../api";

export default function ProgressPage() {
  const { taskId } = useParams();
  const navigate = useNavigate();

  const intervalRef = useRef(null);

  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("Starting...");
  const [error, setError] = useState("");

  useEffect(() => {
    const poll = async () => {
      try {
        const data = await getProgress(taskId);

        if (data.error) {
          setError(data.error);
          clearInterval(intervalRef.current);
          return;
        }

        setProgress(data.progress || 0);
        setMessage(data.message || "Processing...");

        if (data.progress >= 100) {
          clearInterval(intervalRef.current);

          setTimeout(() => {
            navigate(`/result/${taskId}`);
          }, 1200);
        }
      } catch {
        setError(
          "Connection lost. Please make sure the backend server is running."
        );
        clearInterval(intervalRef.current);
      }
    };

    poll();

    intervalRef.current = setInterval(poll, 1500);

    return () => clearInterval(intervalRef.current);
  }, [taskId, navigate]);

  const steps = [
    {
      icon: <FiUploadCloud />,
      title: "Uploading",
      done: progress >= 10,
    },
    {
      icon: <FiFileText />,
      title: "Reading PDF",
      done: progress >= 25,
    },
    {
      icon: <FiCpu />,
      title: "OCR",
      done: progress >= 50,
    },
    {
      icon: <FiGlobe />,
      title: "Translation",
      done: progress >= 80,
    },
    {
      icon: <FiCheckCircle />,
      title: "Generating PDF",
      done: progress >= 100,
    },
  ];

  if (error) {
    return (
      <div className="page-container">
        <GlassCard>

          <div style={{ textAlign: "center" }}>
            <FiAlertCircle
              size={70}
              color="#ef4444"
            />

            <h1
              className="title"
              style={{ marginTop: 20 }}
            >
              Something Went Wrong
            </h1>

            <p className="subtitle">
              {error}
            </p>

            <button
              className="glass-button"
              onClick={() => navigate("/")}
            >
              Try Again
            </button>
          </div>

        </GlassCard>
      </div>
    );
  }

  return (
    <div className="page-container">

      <GlassCard>

        <motion.div
          initial={{
            opacity: 0,
            y: -20,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
        >

          <h1 className="title">
            AI Translation In Progress
          </h1>

          <p className="subtitle">
            Please wait while your document is processed.
          </p>

        </motion.div>

        <div
          className="progress-bar-container"
          style={{
            marginTop: 35,
          }}
        >

          <motion.div
            className="progress-bar-fill"
            initial={{
              width: 0,
            }}
            animate={{
              width: `${progress}%`,
            }}
            transition={{
              duration: 0.5,
            }}
          />

        </div>

        <motion.h2
          style={{
            textAlign: "center",
            marginTop: 25,
            fontSize: "3rem",
            color: "#A78BFA",
          }}
          key={progress}
          initial={{
            scale: 0.9,
          }}
          animate={{
            scale: 1,
          }}
        >
          {progress}%
        </motion.h2>

        <p
          className="status-text"
          style={{
            marginBottom: 30,
          }}
        >
          {message}
        </p>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 18,
          }}
        >
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{
                opacity: 0,
                x: -20,
              }}
              animate={{
                opacity: 1,
                x: 0,
              }}
              transition={{
                delay: index * 0.1,
              }}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 14,
                padding: 14,
                borderRadius: 14,
                background: step.done
                  ? "rgba(34,197,94,.12)"
                  : "rgba(255,255,255,.05)",
                border: step.done
                  ? "1px solid rgba(34,197,94,.25)"
                  : "1px solid rgba(255,255,255,.08)",
              }}
            >
              <div
                style={{
                  fontSize: 24,
                  color: step.done
                    ? "#22c55e"
                    : "#a78bfa",
                }}
              >
                {step.done ? (
                  <FiCheckCircle />
                ) : (
                  step.icon
                )}
              </div>

              <div
                style={{
                  flex: 1,
                  fontWeight: 600,
                }}
              >
                {step.title}
              </div>

              {step.done ? (
                <span
                  style={{
                    color: "#22c55e",
                    fontWeight: 700,
                  }}
                >
                  Done
                </span>
              ) : (
                <FiLoader
                  className="spinner"
                />
              )}
            </motion.div>
          ))}
        </div>

        {progress === 0 && (
          <p
            style={{
              textAlign: "center",
              marginTop: 25,
              opacity: 0.6,
              fontSize: ".9rem",
            }}
          >
            First launch may take a few minutes while AI
            models load into memory.
          </p>
        )}

      </GlassCard>

    </div>
  );
}