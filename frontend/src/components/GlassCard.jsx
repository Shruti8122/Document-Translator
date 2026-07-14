import { motion } from "framer-motion";
import "../styles/glassmorphism.css";

export default function GlassCard({ children, className = "" }) {
  return (
    <motion.div
      className={`glass-card ${className}`}
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.45,
      }}
    >
      {children}
    </motion.div>
  );
}