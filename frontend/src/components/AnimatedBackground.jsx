import { motion } from "framer-motion";
import "../styles/background.css";

export default function AnimatedBackground() {
    return (
        <div className="background">
            <motion.div
                className="blob blob1"
                animate={{
                    x: [0, 80, 0],
                    y: [0, -60, 0],
                    scale: [1, 1.2, 1],
                }}
                transition={{
                    duration: 18,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
            />

            <motion.div
                className="blob blob2"
                animate={{
                    x: [0, -70, 0],
                    y: [0, 90, 0],
                    scale: [1, 1.3, 1],
                }}
                transition={{
                    duration: 22,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
            />

            <motion.div
                className="blob blob3"
                animate={{
                    x: [0, 50, 0],
                    y: [0, 80, 0],
                    scale: [1, 1.15, 1],
                }}
                transition={{
                    duration: 20,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
            />

            <div className="grid-overlay" />
        </div>
    );
}