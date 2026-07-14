import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  FiCheckCircle,
  FiDownload,
  FiHome,
  FiFileText,
  FiEye,
} from "react-icons/fi";

import GlassCard from "../components/GlassCard";
import { getDownloadUrl, getResultUrl } from "../api";

export default function ResultPage() {

  const { taskId } = useParams();

  const navigate = useNavigate();

  const [ready, setReady] = useState(false);

  useEffect(() => {

    setReady(true);

  }, [taskId]);

  const pdfUrl = getResultUrl(taskId);

  const downloadUrl = getDownloadUrl(taskId);

  return (

    <div className="page-container result-page">

      <GlassCard className="result-card">

        <motion.div

          initial={{
            opacity: 0,
            y: -20
          }}

          animate={{
            opacity: 1,
            y: 0
          }}

        >

          <div
            style={{
              textAlign: "center"
            }}
          >

            <FiCheckCircle

              size={70}

              color="#22c55e"

            />

          </div>

          <h1 className="title">

            Translation Complete

          </h1>

          <p className="subtitle">

            Your translated PDF has been generated successfully.

          </p>

        </motion.div>

        <div

          style={{

            display: "grid",

            gridTemplateColumns: "repeat(auto-fit,minmax(140px,1fr))",

            gap: 15,

            marginTop: 30,

            marginBottom: 30

          }}

        >

          <div className="info-card">

            <FiFileText
              size={30}
            />

            <h3>PDF Ready</h3>

            <p>Generated Successfully</p>

          </div>

          <div className="info-card">

            <FiEye
              size={30}
            />

            <h3>Preview</h3>

            <p>View Before Download</p>

          </div>

        </div>

        {

          ready && (

            <motion.iframe

              initial={{
                opacity: 0
              }}

              animate={{
                opacity: 1
              }}

              transition={{
                duration: .5
              }}

              src={pdfUrl}

              title="Translated PDF"

              className="pdf-embed"

            />

          )

        }

        <div className="button-group">

          <a

            href={downloadUrl}

            download

            className="glass-button"

            style={{
              textDecoration: "none",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: 10,
              flex: 1
            }}

          >

            <FiDownload />

            Download PDF

          </a>

          <button

            className="glass-button secondary-button"

            onClick={() => navigate("/")}

          >

            <FiHome
              style={{
                marginRight: 8
              }}
            />

            Translate Another

          </button>

        </div>

      </GlassCard>

    </div>

  );

}