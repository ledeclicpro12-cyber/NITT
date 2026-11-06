import { Composition } from "remotion";
import { Solitude, FPS } from "./Solitude";
import { Cover } from "./Cover";
import timeline from "./timeline.json";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Solitude"
      component={Solitude}
      durationInFrames={Math.ceil((timeline as any).total * FPS)}
      fps={FPS}
      width={1080}
      height={1920}
    />
    <Composition id="Cover" component={Cover} durationInFrames={1} fps={FPS} width={1080} height={1920} />
  </>
);
