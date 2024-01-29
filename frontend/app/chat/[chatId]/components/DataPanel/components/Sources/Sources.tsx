import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { Source } from "@/lib/types/MessageMetadata";

import styles from "./Sources.module.scss";

interface SourcesProps {
  sources?: Source[];
}

const Sources = ({ sources }: SourcesProps): JSX.Element => {
  return (
    <FoldableSection label="Sources" icon="file">
      <div className={styles.sources_wrapper}>
        {sources?.map((source, index) => (
          <a
            href={source.source_url}
            key={index}
            target="_blank"
            rel="noopener noreferrer"
          >
            <div className={styles.source}>{source.name}</div>
          </a>
        ))}
      </div>
    </FoldableSection>
  );
};

export default Sources;
