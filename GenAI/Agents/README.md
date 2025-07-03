```mermaid
flowchart TD
    START([🚀 START<br/>Event Planning Request]) 
    
    START --> INPUT[/📝 INPUT<br/>Conference Details<br/>Venue Requirements<br/>Budget & Constraints<br/>Timeline/]
    
    INPUT --> PREP{{🏗️ PREPARATION<br/>Initialize Crew System<br/>Load Agent Configurations<br/>Enable Memory & Tools}}
    
    PREP --> PROCESS1[⚡ PROCESS<br/>Crew Kickoff<br/>Begin Sequential Execution]
    
    PROCESS1 --> TASK1_INIT{{📋 PREPARATION<br/>Initialize Task 1<br/>Venue Finding Task<br/>Set Priority & Goals}}
    
    TASK1_INIT --> ASSIGN1[🤖 PROCESS<br/>Assign Venue Finder Agent<br/>Role: Conference Venue Specialist<br/>Load Tools & Capabilities]
    
    ASSIGN1 --> SEARCH_OP[🔍 PROCESS<br/>Execute Search Operations<br/>Query Online Databases<br/>Filter by Criteria<br/>Gather Information]
    
    SEARCH_OP --> SEARCH_CHECK{📊 DECISION<br/>Venues Found?<br/>Quality Check Passed?<br/>Meets Requirements?}
    
    SEARCH_CHECK -->|No| RETRY{{🔄 PREPARATION<br/>Adjust Search Strategy<br/>Broaden Criteria<br/>Try Alternative Methods}}
    
    RETRY --> SEARCH_OP
    
    SEARCH_CHECK -->|Yes| PROCESS_DATA[⚙️ PROCESS<br/>Process Venue Data<br/>Parse Details<br/>Format Results<br/>Validate Information]
    
    PROCESS_DATA --> OUTPUT1[/📤 OUTPUT<br/>Task 1 Results<br/>Venue List<br/>Specifications<br/>Pricing Data/]
    
    OUTPUT1 --> MEMORY_STORE[(💾 STORAGE<br/>Store in Memory<br/>Save Results<br/>Preserve Context)]
    
    MEMORY_STORE --> TASK2_INIT{{📋 PREPARATION<br/>Initialize Task 2<br/>Quality Assurance<br/>Set Review Parameters}}
    
    TASK2_INIT --> ASSIGN2[🤖 PROCESS<br/>Assign QA Agent<br/>Role: Quality Specialist<br/>Access Memory System]
    
    ASSIGN2 --> MEMORY_GET[(🔍 STORAGE<br/>Retrieve from Memory<br/>Load Previous Results<br/>Access Requirements)]
    
    MEMORY_GET --> QA_PROCESS[🔎 PROCESS<br/>Quality Review<br/>Check Against Standards<br/>Identify Issues<br/>Assess Suitability]
    
    QA_PROCESS --> QA_DECISION{✅ DECISION<br/>Quality Standards Met?<br/>Issues Found?<br/>Approval Status?}
    
    QA_DECISION -->|Rejected| FEEDBACK[/📝 OUTPUT<br/>Generate Feedback<br/>List Issues<br/>Improvement Suggestions/]
    
    FEEDBACK --> TASK1_INIT
    
    QA_DECISION -->|Approved| FINAL_PROCESS[📋 PROCESS<br/>Generate Final Report<br/>Create Recommendations<br/>Prepare Deliverables]
    
    FINAL_PROCESS --> OUTPUT2[/📤 OUTPUT<br/>Final Report<br/>Quality Assessment<br/>Recommendations<br/>Action Items/]
    
    OUTPUT2 --> FINAL_CHECK{🎯 DECISION<br/>All Tasks Complete?<br/>Standards Met?<br/>Ready for Delivery?}
    
    FINAL_CHECK -->|No| ERROR_HANDLE[❌ PROCESS<br/>Handle Errors<br/>Log Issues<br/>Retry Operations]
    
    ERROR_HANDLE --> TASK1_INIT
    
    FINAL_CHECK -->|Yes| SUCCESS[✅ PROCESS<br/>Mark Complete<br/>Record Success Metrics<br/>Prepare Delivery]
    
    SUCCESS --> END([🎉 END<br/>Process Complete<br/>Client Deliverable Ready])
    
    subgraph legend [📋 FLOWCHART LEGEND]
        L1([Oval: Start/End Terminators])
        L2[Rectangle: Process Steps]
        L3{Diamond: Decision Points}
        L4[/Parallelogram: Input/Output/]
        L5{{Hexagon: Preparation Steps}}
        L6[(Cylinder: Data Storage)]
    end
    
    subgraph agents [🤖 AGENT SYSTEM]
        VF[Venue Finder Agent<br/>• Search Specialist<br/>• Venue Expert<br/>• Tool Access]
        QA[Quality Assurance Agent<br/>• Review Expert<br/>• Standards Validator<br/>• Memory Access]
    end
    
    subgraph memory [💾 MEMORY SYSTEM]
        STM[(Short-term Memory<br/>Session Data<br/>Task Results)]
        LTM[(Long-term Memory<br/>Historical Data<br/>Patterns)]
    end
    
    subgraph tools [🛠️ TOOL ECOSYSTEM]
        ST[Search Tool<br/>Web APIs<br/>Data Parsing]
        CT[Custom Tools<br/>Databases<br/>Validators]
    end
    
    style START fill:#e8f5e8,stroke:#2e7d32,stroke-width:3px
    style END fill:#e8f5e8,stroke:#2e7d32,stroke-width:3px
    style SUCCESS fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    style ERROR_HANDLE fill:#ffcdd2,stroke:#d32f2f,stroke-width:3px
    style SEARCH_CHECK fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style QA_DECISION fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style FINAL_CHECK fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style ASSIGN1 fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style ASSIGN2 fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style MEMORY_STORE fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style MEMORY_GET fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
