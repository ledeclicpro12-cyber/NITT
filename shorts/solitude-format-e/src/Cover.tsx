import React from "react";
import { AbsoluteFill } from "remotion";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadFraunces } from "@remotion/google-fonts/Fraunces";

export const Cover: React.FC = () => {
  const inter = loadInter("normal", { weights: ["700"], subsets: ["latin"] }).fontFamily;
  const fraunces = loadFraunces("italic", { weights: ["600"], subsets: ["latin"] }).fontFamily;

  return (
    <AbsoluteFill
      style={{
        background: "#0E1220",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 32,
      }}
    >
      <div
        style={{
          fontFamily: inter,
          fontWeight: 700,
          fontSize: 52,
          color: "#A9C6E8",
          textAlign: "center",
          padding: "0 80px",
          letterSpacing: -0.5,
        }}
      >
        T'as besoin d'être seul après avoir vu des gens que t'aimes.
      </div>
      <div
        style={{
          fontFamily: fraunces,
          fontWeight: 600,
          fontSize: 36,
          fontStyle: "italic",
          color: "#F2A65A",
          textAlign: "center",
        }}
      >
        C'est de la récupération.
      </div>
    </AbsoluteFill>
  );
};
