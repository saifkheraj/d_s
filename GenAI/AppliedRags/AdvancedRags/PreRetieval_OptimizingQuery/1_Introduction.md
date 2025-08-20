flowchart LR
    A[User Query] --> B[Query Optimization]
    B --> C[Retriever]
    C --> D[Vector Store]
    D --> E[Post-Retrieval Techniques]
    E --> F[Large Language Model]
    F --> G[Response]

    subgraph Indexing
        H[Raw Data] --> I[Index Optimization]
        I --> D
    end

    subgraph Index Optimization
        I1[Chunk optimization]
        I2[Enhancing data granularity]
        I3[Multi-representation indexing]
        I4[Self-querying retrieval]
        I5[Parent document retrieval]
        I1 --> I
        I2 --> I
        I3 --> I
        I4 --> I
        I5 --> I
    end

    subgraph Query Optimization
        Q1[Multi query]
        Q2[Decomposition]
        Q3[HyDE]
        Q4[Step-back]
        Q5[Semantic routing]
        Q6[Routing with classifier]
        Q1 --> B
        Q2 --> B
        Q3 --> B
        Q4 --> B
        Q5 --> B
        Q6 --> B
    end

    subgraph Post-Retrieval Techniques
        P1[Re-ranking]
        P2[Context compression]
        P3[Cross-Encoder re-ranking]
        P4[RAG-Fusion]
        P1 --> E
        P2 --> E
        P3 --> E
        P4 --> E
    end
