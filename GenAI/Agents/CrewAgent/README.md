```mermaid
graph TD
    %% Root
    START([🚀 START EXECUTION])
    
    %% Main execution branches
    START --> STEP1[1️⃣ CREW INITIALIZATION]
    START --> STEP2[2️⃣ TASK ASSIGNMENT]
    START --> STEP3[3️⃣ SEQUENTIAL EXECUTION]
    START --> STEP4[4️⃣ FINAL RESULT]
    
    %% Step 1 details
    STEP1 --> S1_CREATE[📋 Create Crew Instance]
    STEP1 --> S1_LOAD[🤖 Load 2 Agents]
    STEP1 --> S1_DEFINE[📝 Define 2 Tasks]
    STEP1 --> S1_SETUP[🛠️ Setup Tools]
    STEP1 --> S1_MEMORY[(🧠 Enable Memory)]
    
    %% Step 2 details
    STEP2 --> S2_TASK1[📋 Task 1 → Venue Finder Agent]
    STEP2 --> S2_TASK2[📋 Task 2 → QA Agent]
    STEP2 --> S2_ORDER[🔄 Set Sequential Order]
    
    %% Step 3 details - Sequential execution
    STEP3 --> S3_FIRST[🔍 FIRST TASK EXECUTION]
    STEP3 --> S3_SECOND[✅ SECOND TASK EXECUTION]
    
    %% First execution details
    S3_FIRST --> S3F_CREW_CALLS[🎭 CREW calls Task 1]
    S3F_CREW_CALLS --> S3F_TASK_ASSIGNS[📋 Task 1 assigns to Venue Finder Agent]
    S3F_TASK_ASSIGNS --> S3F_AGENT_STARTS[🔍 Venue Finder Agent starts working]
    S3F_AGENT_STARTS --> S3F_TOOL[🌐 Agent uses Search Tool]
    S3F_TOOL --> S3F_FIND[🏢 Agent finds venues]
    S3F_FIND --> S3F_SAVE[(💾 Agent saves to Memory)]
    S3F_SAVE --> S3F_REPORTS{📤 Agent reports back to CREW}
    S3F_REPORTS --> S3F_DONE[✅ CREW marks Task 1 complete]
    
    %% Second execution details
    S3_SECOND --> S3S_CREW_CALLS[🎭 CREW calls Task 2]
    S3S_CREW_CALLS --> S3S_TASK_ASSIGNS[📋 Task 2 assigns to QA Agent]
    S3S_TASK_ASSIGNS --> S3S_AGENT_STARTS[✅ QA Agent starts working]
    S3S_AGENT_STARTS --> S3S_READ[(🧠 Agent reads Memory)]
    S3S_READ --> S3S_TOOL[🌐 Agent uses Search Tool]
    S3S_TOOL --> S3S_REVIEW[🔍 Agent reviews venues]
    S3S_REVIEW --> S3S_ASSESS[📊 Agent creates assessment]
    S3S_ASSESS --> S3S_REPORTS{📤 Agent reports back to CREW}
    S3S_REPORTS --> S3S_DONE[✅ CREW marks Task 2 complete]
    
    %% Step 4 details
    STEP4 --> S4_COMPILE[📋 Compile All Results]
    S4_COMPILE --> S4_DELIVER[/🎉 Deliver to User/]
    S4_DELIVER --> END([✨ END])
    
    %% Key insight box
    INSIGHT[💡 CLEAR EXECUTION FLOW<br/>1. CREW calls Task<br/>2. Task assigns to Agent<br/>3. Agent does the work<br/>4. Agent reports back to CREW<br/>5. CREW moves to next Task]
    
    END --> INSIGHT
    
    %% Styling
    classDef startEnd fill:#e8f5e8,stroke:#4caf50,stroke-width:4px
    classDef step fill:#e3f2fd,stroke:#2196f3,stroke-width:3px
    classDef detail fill:#f5f5f5,stroke:#757575,stroke-width:2px
    classDef execution fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef memory fill:#fff8e1,stroke:#fbc02d,stroke-width:3px
    classDef decision fill:#fce4ec,stroke:#e91e63,stroke-width:2px
    classDef io fill:#e0f2f1,stroke:#009688,stroke-width:2px
    classDef insight fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px
    
    class START,END startEnd
    class STEP1,STEP2,STEP3,STEP4 step
    class S1_CREATE,S1_LOAD,S1_DEFINE,S1_SETUP,S2_TASK1,S2_TASK2,S2_ORDER,S4_COMPILE detail
    class S3_FIRST,S3_SECOND,S3F_CREW_CALLS,S3F_TASK_ASSIGNS,S3F_AGENT_STARTS,S3F_TOOL,S3F_FIND,S3F_DONE,S3S_CREW_CALLS,S3S_TASK_ASSIGNS,S3S_AGENT_STARTS,S3S_TOOL,S3S_REVIEW,S3S_ASSESS,S3S_DONE execution
    class S1_MEMORY,S3F_SAVE,S3S_READ memory
    class S3F_REPORTS,S3S_REPORTS decision
    class S4_DELIVER io
    class INSIGHT insight
