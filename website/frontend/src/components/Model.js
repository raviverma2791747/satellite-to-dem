import React from "react";
import nasaDEM from "../assets/models/output_NASADEM.stl";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import { Canvas, useLoader, useThree } from "@react-three/fiber";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader";
import { MTLLoader } from "three/examples/jsm/loaders/MTLLoader";
import { TextureLoader } from 'three/src/loaders/TextureLoader'

const Model = ({ url, texture }) => {
    const colorMap = useLoader(TextureLoader, URL.createObjectURL(texture))
    const materials = useLoader(MTLLoader, "Poimandres.mtl");
    const geom = useLoader(STLLoader, url, (loader) => {
       console.log(loader)
  });

  const ref = React.useRef();
  const { camera } = useThree();
  React.useEffect(() => {
    camera.lookAt(ref.current.position);
  });

  return (
    <>
      <mesh ref={ref} position={[0, 0, 0]}>
              <primitive object={geom} position={[0, 0, 0]} />
              <meshBasicMaterial map={colorMap} />
      </mesh>
      <ambientLight />
      <pointLight position={[10, 10, 10]} />
    </>
  );
};

export default Model;
