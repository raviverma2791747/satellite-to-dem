import React, { Suspense, lazy } from "react";
import { Canvas } from "@react-three/fiber";
import {
  Html,
  useProgress,
  OrbitControls,
  Environment,
} from "@react-three/drei";

const Model = lazy(() => import("./Model"));

const Loading = () => {
  const { progress } = useProgress();
  return <Html center>{progress} % loaded</Html>;
};
const Viewer = ({texture}) => {
  return (
    <Canvas className="border border-dark" style={{ width: "25vw", height: "25vw" }}>
      <Suspense fallback={<Loading />}>
        <Model url={"http://127.0.0.1:5000/api/model/download/output_NASADEM.stl"} texture={texture} />
        <OrbitControls />
        <Environment preset="warehouse" />
        <axesHelper/>
      </Suspense>
    </Canvas>
  );
};

export default Viewer;
