# **The Semantic Shift: Integrating Agentic AI, Vibe Coding, and Advanced Pedagogy in Computer Science Education**

## **1\. Introduction: The Post-Syntax Era of Software Engineering**

The discipline of computer science stands at a precipice of transformation as significant as the transition from assembly language to high-level compilers. For decades, the barrier to entry for software creation was syntax—the rigorous, unforgiving grammatical rules of languages like Python and JavaScript. Mastery of these languages was the gatekeeper of the digital realm. However, the convergence of Large Language Models (LLMs), agentic workflows, and a new cultural practice known as "vibe coding" has fundamentally altered this landscape. We are witnessing the birth of a "post-syntax" era where natural language—specifically English—serves as the primary compilation layer for computational logic.

This report provides an exhaustive analysis of this paradigm shift. It examines the emergence of "vibe coding" not merely as a trend, but as a distinct developmental methodology championed by industry leaders like Andrej Karpathy. It analyzes the technological infrastructure enabling this shift, from the autonomous "wide research" capabilities of the **Manus** agent to the integrated "flow" states provided by AI-native editors like **Cursor** and **Windsurf**. Furthermore, it explores the critical role of **NotebookLM** as a cognitive scaffold for learning and synthesis in an information-dense environment.

However, the democratization of code generation introduces profound risks regarding correctness, maintainability, and bias. Consequently, this report delves into the emerging landscape of AI benchmarking—ironically typified by the user's query "Beacvhmarch"—analyzing the **SWE-bench**, **BigCodeBench**, and specialized metrics like **Beaver** (enterprise SQL) and **Bee** (ethical computer vision). Finally, we propose a radical restructuring of pedagogical methods ("métodos de ensino"). We argue that traditional frameworks like **PRIMM** (Predict, Run, Investigate, Modify, Make) and the **Flipped Classroom** must be recalibrated to prioritize "evaluative competence" over rote memorization, ensuring that students remain the architects of systems they no longer manually build brick by brick.

## ---

**2\. The Phenomenology of Vibe Coding: From Meme to Methodology**

### **2.1 Defining the Indefinable: The "Vibe" as Technical Specification**

"Vibe coding" entered the technical lexicon in February 2025, coined by Andrej Karpathy, a former director of AI at Tesla and co-founder of OpenAI.1 While initially circulated as a meme on social media platforms like X (formerly Twitter), the concept crystallized a profound shift in developer-machine interaction. Karpathy defined vibe coding as a state where the human programmer "fully gives in to the vibes," embracing the exponential capabilities of LLMs and, crucially, "forgetting that the code even exists".2

This definition challenges the foundational dogma of software engineering, which prioritizes deterministic control and granular understanding. In a "pure" vibe coding workflow, the developer operates almost exclusively through natural language prompts, accepting the AI's output without rigorous line-by-line inspection.3 The focus shifts from the *process* of writing code to the *outcome* or the "vibe" of the running application. If the application behaves as intended—if the button clicks, the animation flows, and the data loads—the code is deemed "correct," regardless of its underlying structure.2

#### **2.1.1 The Spectrum of Responsibility: "Pure" vs. "Responsible"**

A critical distinction has emerged in the discourse, separating "Pure Vibe Coding" from "Responsible AI-Assisted Development".1

* **Pure Vibe Coding:** This mode is characterized by rapid iteration and low inhibition. It is best suited for what Karpathy terms "throwaway weekend projects"—prototypes, personal tools, or experimental interfaces where long-term maintainability is secondary to immediate functionality.2 In this mode, the user acts as a creative director, guiding the AI through high-level desires ("make it pop," "fix that weird spacing") rather than technical specifications. The risk, as noted by critics like Simon Willison, is "maintainability debt." If a vibe-coded project breaks and the AI cannot fix it, the user—having never understood the code—is left helpless.2  
* **Responsible AI-Assisted Development:** Often conflated with vibe coding, this approach utilizes the same conversational interfaces but retains the rigors of engineering. Here, the developer acts as a "Senior Engineer" to the AI's "Junior." The developer prompts the AI for code but reviews, tests, and refines the output, ensuring adherence to security standards and architectural patterns.1 IBM and other enterprise players emphasize this model, viewing AI as a "pair programmer" that augments rather than replaces human judgment.4

### **2.2 The Democratization of Creation**

The most significant impact of vibe coding is the lowering of the "sunk cost" barrier.4 Traditionally, validating a software idea required significant investment in coding time. Vibe coding allows for "near-instant prototyping," enabling non-technical domain experts—marketing managers, biologists, writers—to spin up functional beta versions of products in minutes.5 This capability was highlighted by Google CEO Sundar Pichai, who noted that vibe coding allows non-tech graduates to build careers in technology, fundamentally reshaping the demographics of the software workforce.6

However, this democratization is not without friction. University students, steeped in the belief that "learning to code" means "learning syntax," have expressed frustration at curriculums that embrace vibe coding, viewing it as an invalidation of their tuition and effort.7 This tension between the *labor* of coding and the *value* of software is the central conflict of modern computer science education.

### **2.3 The Tooling of Vibes: Natural Language as the IDE**

The transition to vibe coding is facilitated by a new class of tools that treat English as a first-class citizen.

* **English as Syntax:** As Karpathy famously stated, "the hottest new programming language is English".3 This is not metaphorical; modern LLMs can parse intent from colloquialisms ("make the header less angry") and translate them into precise CSS or JavaScript.  
* **The Feedback Loop:** The vibe coding workflow is cyclical: Describe Goal $\\rightarrow$ AI Generates $\\rightarrow$ Execute and Observe $\\rightarrow$ Refine via Feedback.1 This loop replaces the traditional "Write $\\rightarrow$ Compile $\\rightarrow$ Debug" cycle, significantly tightening the iteration time and allowing for a "flow state" that was previously difficult to maintain when wrestling with syntax errors.

## ---

**3\. The Agentic Infrastructure: Manus, Cursor, and the New Stack**

While "vibe coding" describes the *workflow*, the feasibility of this workflow depends entirely on the sophistication of the underlying AI agents. We have moved beyond simple "chatbots" to "Agentic AI"—systems capable of planning, executing, and correcting complex chains of actions.

### **3.1 Manus: The Autonomous Action Engine**

**Manus** represents the vanguard of this agentic shift. Unlike a standard LLM that generates text, Manus is designed as an "action engine" capable of executing tasks autonomously.8 Its architecture addresses one of the fundamental limitations of previous AI models: the inability to handle scale and complexity without degradation.

#### **3.1.1 The "Wide Research" Architecture**

A persistent failure mode of LLMs is "context drift" or the "lost in the middle" phenomenon, where the model's performance degrades as it processes a long sequence of tasks. Manus introduces a proprietary architecture known as **"Wide Research"** to solve this.9

* **Parallel Processing:** Instead of processing a request like "Analyze these 50 companies" sequentially (which would lead to detailed analysis for the first few and generic summaries for the last), Manus decomposes the task and spawns independent agents for *each* item.9  
* **Context Isolation:** Each sub-agent operates in its own dedicated context window/virtual environment.10 This ensures that the 50th company receives the exact same depth of cognitive resource and analysis as the first.  
* **Synthesis:** A central orchestrator then collects the results from these parallel agents and synthesizes them into a structured report or dataset. This capability is revolutionary for educational research and market analysis, allowing students to perform literature reviews of unprecedented scale.10

#### **3.1.2 Self-Correction and The "Loop"**

Manus distinguishes itself from "Copilots" by its autonomy. It operates on a "Human-on-the-loop" model rather than "Human-in-the-loop".11 When Manus encounters an error (e.g., a failed web scrape or a syntax error in generated code), it attempts to self-correct without interrupting the user. It can debug its own execution steps, refine its strategy, and only report back when the task is complete or irresolvable.11 This "agentic" behavior allows for true asynchronous productivity—a student can assign Manus a research task and go to sleep, waking up to a completed report.

#### **3.1.3 Use Cases in Education and Industry**

The application of Manus extends far beyond simple code generation.

* **Education:** At **Heicoders Academy**, students use Manus to build "Skin Analysis Websites" and "SOP Builders." The tool allows them to bridge the gap between conceptual design and technical implementation, managing projects that would otherwise require a full development team.12  
* **Complex Workflows:** Manus can execute end-to-end workflows like "Plan a trip to Japan," where it not only finds flights but creates a detailed itinerary based on user preferences, checking weather and local events.13 In finance, it can generate stock market analyses and interactive dashboards, processing complex datasets that would overwhelm a standard chatbot.13

### **3.2 The Battle for the Editor: Cursor vs. Windsurf**

While Manus handles autonomous tasks, the day-to-day work of coding still largely happens in an Integrated Development Environment (IDE). The market has seen a divergence between "AI-augmented" editors and "AI-native" editors.

#### **3.2.1 Cursor: The Vibe Coder's Choice**

**Cursor**, a fork of VS Code, has become the de facto standard for vibe coding.14 Its dominance lies in its "Composer" feature, which allows users to edit multiple files simultaneously using natural language.

* **Tab Autocomplete:** Cursor’s "Tab" feature goes beyond simple line completion. It predicts the *next edit*, often suggesting entire blocks of code based on the user's recent changes in other files.14 This anticipation maintains the developer's "flow state."  
* **Privacy and Control:** Cursor offers a "Privacy Mode" where code is not stored on their servers, addressing enterprise security concerns.16 It supports a variety of backend models, including Claude 3.5 Sonnet and GPT-4o, giving users control over the "intelligence" driving their editor.14

#### **3.2.2 Windsurf: The "Cascade" Approach**

**Windsurf** enters the arena as a direct competitor, focusing on a concept called "Cascade".17

* **Deep Context Awareness:** Windsurf emphasizes a deeper understanding of the project's entire codebase "context." While Cursor is excellent at local edits, Windsurf aims to understand the *implications* of a change across the entire repository.17  
* **Flow State:** Like Cursor, it prioritizes keeping the developer "in the zone," minimizing the friction between thought and code implementation.16

**Table 1: Comparative Analysis of Agentic Tools**

| Feature | Manus | Cursor | Windsurf |
| :---- | :---- | :---- | :---- |
| **Primary Paradigm** | Autonomous Agent (Task Executor) | AI-Powered Editor (Code Assistant) | Flow-State IDE (Context Aware) |
| **Interaction Model** | "Go do this" (Asynchronous) | "Help me write this" (Synchronous) | "Collaborate with me" (Synchronous) |
| **Key Architecture** | Wide Research (Parallel Agents) | Composer (Multi-file Editing) | Cascade (Deep Context Flow) |
| **Best Use Case** | Research, Data Analysis, Full App Gen | Refactoring, Vibe Coding, Debugging | Project-wide Navigation, Development |
| **User Role** | Supervisor / Orchestrator | Driver / Pilot | Co-Pilot / Collaborator |

### **3.3 NotebookLM: The Synthesis Engine**

In an era of infinite information generation by AI, the bottleneck shifts to human comprehension. **NotebookLM** addresses this by serving as a "grounded" synthesis engine.18

* **Source Grounding:** Unlike general chatbots that rely on their training data (and thus hallucinate), NotebookLM answers questions *only* based on the documents uploaded by the user.19 This "RAG-as-a-Service" model is critical for education, ensuring that students are learning from verified course materials rather than the internet's collective noise.  
* **Audio Overviews:** Perhaps its most innovative feature is the ability to generate "Deep Dive" audio discussions. Two AI hosts banter about the uploaded content, using metaphors and dialogue to explain complex concepts.20 This multimodal approach caters to auditory learners and provides a "social" learning experience even in isolation.  
* **Privacy First:** Google explicitly states that NotebookLM does not train its models on user data, making it safe for corporate and academic use.19

## ---

**4\. The "Beacvhmarch" Crisis: Benchmarking in the Age of AI**

The user's query included the term "Beacvhmarch," a misspelling of "Benchmark." This slip is symbolic of the current state of AI evaluation: messy, evolving, and critical. As AI models saturate traditional benchmarks like HumanEval (where they achieve near-perfect scores), the industry has had to invent new, harder, and more realistic tests to differentiate "toy" models from "engineering" models.

### **4.1 SWE-bench: The Engineering Standard**

**SWE-bench** (Software Engineering Benchmark) has emerged as the gold standard for assessing an AI's ability to function as a software engineer.21

* **Real-World Complexity:** Unlike LeetCode problems which are self-contained algorithmic puzzles, SWE-bench tasks are drawn from real GitHub issues in popular open-source libraries (e.g., Django, scikit-learn).21 The AI is given a codebase and an issue description and must generate a "patch" that resolves the issue and passes new test cases.  
* **The Verified Leaderboard:** Early iterations of SWE-bench suffered from "unsolvable" issues—bugs that were poorly described or required external context. The **SWE-bench Verified** subset was released to address this, providing a human-validated set of solvable tasks.22  
* **Performance Reality Check:** As of late 2025, top models like Claude 3.5 Sonnet and GPT-4o achieve scores in the **40-70%** range on SWE-bench Verified.23 This statistic is vital for educators: it quantifies exactly how much "human" is still needed. AI is not a replacement; it is a mid-level contributor that fails 30-60% of the time on complex tasks.

### **4.2 BigCodeBench: The "Gluing" Test**

While SWE-bench tests bug fixing, **BigCodeBench** evaluates the "vibe coding" skill of gluing libraries together.24

* **Library Diversity:** It consists of 1,140 tasks requiring the use of 139 different libraries.24 This mirrors the modern developer's workflow, which is less about writing sorting algorithms and more about invoking pandas, pytorch, or react functions correctly.  
* **Instruction Following:** It specifically tests the model's ability to follow complex, multi-step natural language instructions, a prerequisite for effective vibe coding.24

### **4.3 Beaver: The Enterprise SQL Reality**

The **Beaver** benchmark addresses a specific blind spot: Enterprise Data Warehouses.25

* **The Gap:** Most Text-to-SQL benchmarks use simple, public databases. Enterprise databases, however, are massive, messy, and proprietary.  
* **The Benchmark:** Beaver collects queries from real private organizations. It features complex schemas with high "nesting depth" and requirements for multiple joins and aggregations.27  
* **Findings:** LLMs perform significantly worse on Beaver than on academic benchmarks. This highlights that while "vibe coding" might work for a startup's clean database, it often crumbles in the face of legacy enterprise data architectures, necessitating a continued focus on deep SQL training for students.

### **4.4 Bee (FHIBE): The Ethical Dimension**

**Sony AI's "Bee"** (Fair Human-Centric Image Benchmark \- FHIBE) introduces ethics into the benchmarking landscape.28

* **The Problem:** Computer vision models are notoriously biased, often performing poorly on underrepresented demographics due to skewed training data.  
* **The Solution:** Bee is a dataset designed explicitly to test *fairness*. It contains images of 2,000 paid participants from 80 countries, collected with full consent and detailed demographic annotations.28  
* **Educational Implication:** This benchmark transforms "AI Ethics" from a philosophy seminar into a computer science lab. Students can be tasked with auditing models against the Bee dataset, measuring bias quantitatively. This teaches a crucial lesson: a model that is 99% accurate but 100% biased against a specific group is a failed model.

## ---

**5\. The Enduring Relevance of Python and JavaScript**

In the "English as a programming language" era, one might question the utility of learning **Python** or **JavaScript**. However, their role has not diminished; it has shifted from *construction* to *verification*.

### **5.1 Python: The Lingua Franca of Agents**

Python remains the dominant language for AI development and data science.4

* **Agent Construction:** While one can use Manus, *building* a Manus-like agent requires Python. Understanding the Python ecosystem (LangChain, PyTorch) is essential for students who want to be the tool-makers, not just tool-users.  
* **Verification:** When Manus performs a financial analysis, it often generates a Python script to process the data. A "vibe coder" who cannot read Python is blindly trusting the black box. A Python-literate user can audit the script, spotting logical errors in the data processing pipeline.4

### **5.2 JavaScript: The Fabric of the Web**

JavaScript (and its superset TypeScript) remains the executable layer of the web.1

* **Frontend Reality:** Vibe coding tools often generate React or Vue components. However, AI struggles with complex state management, often creating "spaghetti code" or introducing subtle UI bugs.30  
* **The Integration Gap:** AI can generate a button, and it can generate a database. Stitching them together securely requires an understanding of asynchronous JavaScript, API calls, and CORS policies—concepts that are often abstracted away by AI until they break.

## ---

**6\. Transforming Pedagogy: "Métodos de Ensino" for the AI Age**

The arrival of these tools demands a "pedagogical pivot." We cannot continue to teach syntax memorization when a keystroke can generate a thousand lines of code. We must adopt methods that emphasize *process*, *evaluation*, and *systemic thinking*.

### **6.1 PRIMM 2.0: Adapting the Classic Model**

The **PRIMM** framework (Predict, Run, Investigate, Modify, Make) is ideal for this transition because it focuses on code comprehension before code writing.31

#### **6.1.1 The AI-Enhanced PRIMM Cycle**

1. **Predict:** Instead of predicting the output of a simple loop, students are given a complex prompt and asked to predict the *structure* of the code the AI will generate. "If I ask for a login page, what security libraries will the AI likely import?".33  
2. **Run (Generate):** Students use the AI (Manus/Cursor) to generate the solution. This is the "Vibe Coding" phase.  
3. **Investigate:** This becomes the core of the lesson. Students use **NotebookLM** to analyze the generated code. "Why did the AI use useEffect here?" "Is this SQL query vulnerable to injection?" The goal is to audit the AI's work.34  
4. **Modify:** The instructor introduces a constraint that breaks the AI's initial solution (e.g., "Scale this to 1 million users"). Students must guide the AI through the refactoring process, intervening manually where the AI gets stuck in loops.1  
5. **Make:** Students orchestrate a novel project, using the AI as a junior developer. The assessment focuses on the *architecture* and the *testing strategy* rather than the volume of code written.35

### **6.2 The Flipped Classroom: From Lecture to Studio**

The **Flipped Classroom** model is supercharged by AI tools.36

* **At Home (Content Absorption):** Students use NotebookLM to engage with lecture materials. They listen to Audio Overviews of the week's topic (e.g., "Graph Theory") and query the notebook to clarify doubts.18 This ensures that every student enters the class with a baseline understanding.  
* **In Class (Active Creation):** The classroom becomes a "Developer Studio." Students work on "Vibe Coding" projects under the supervision of the instructor. The instructor acts as a "Senior Architect," moving between groups to help resolve complex logic errors or architectural blockers that the AI cannot solve.37 This effectively replicates the mentorship dynamic of a real software team.

### **6.3 Parsons Problems: The Syntax Bridge**

**Parsons Problems** (arranging scrambled lines of code) are experiencing a renaissance.38

* **Cognitive Alignment:** Parsons problems align perfectly with the "review" nature of vibe coding. When an AI generates a block of code, the user is essentially solving a mental Parsons problem—verifying that the lines are in the logical order to produce the desired effect.  
* **AI Customization:** Tools like **PuzzleMakerPy** use LLMs to generate infinite, personalized Parsons problems based on student interests (e.g., "Arrange this code to analyze data from your favorite video game").39 This keeps engagement high while drilling the necessary pattern-recognition skills.

## ---

**7\. Case Studies in Educational Innovation**

Real-world implementation of these methods is already yielding insights into the future of learning.

### **7.1 Yale School of Management: The "Coding with Kyle" Initiative**

At Yale SOM, MBA students with no formal CS background participated in a "Coding with Kyle" initiative.40

* **Methodology:** Students used AI tools to build "AI Digital Twins" and "Journal Analyzers."  
* **Insight:** The initiative demonstrated that "computational thinking"—the ability to decompose a problem into logical steps—is distinct from "syntax knowledge." These business students could build complex applications by focusing on the *logic* and letting the AI handle the *syntax*. This suggests a future where CS education expands into Business and Humanities schools as a "creative literacy."

### **7.2 Heicoders Academy: Real-World Impact with Manus**

Heicoders Academy integrated **Manus** into their "Generative AI for Automation" course.12

* **Student Projects:** Students built "Skin Analysis Websites" and "SOP Builders."  
* **Outcome:** The use of Manus allowed students to tackle problems with *real-world complexity* (e.g., dealing with messy, real-time data) that would be impossible in a traditional "sandbox" assignment. The feedback loop was crucial: students learned that AI agents are not magic; they require clear, structured instructions ("Context Engineering") to function correctly.41

### **7.3 University of Pelotas (UFPel): Monitoring the Hybrid Mind**

Researchers at UFPel are conducting a longitudinal study on how students interact with ChatGPT.42

* **Preliminary Findings:** Effective learning occurs not when the student blindly copies the AI, but when they treat the AI as a "knowledgeable peer." The most successful students engage in a dialogue, challenging the AI's assumptions and asking for explanations, effectively applying the "Investigate" phase of PRIMM naturally.

## ---

**8\. Strategic Recommendations and Future Outlook**

### **8.1 The "Sandwich" Curriculum Strategy**

Educators should adopt a "Sandwich" approach to curriculum design:

1. **Bottom Layer (Foundations):** Intensive, manual coding in Python/JS. Students must struggle with syntax to build the mental models of how computers "think." (Weeks 1-4).  
2. **Filling (Vibe Coding/AI):** Introduce Cursor, Manus, and NotebookLM. Unleash creativity. Allow students to build massive, impressive projects using their foundational knowledge to guide the AI. (Weeks 5-10).  
3. **Top Layer (System Internals/Verification):** Return to the deep dive. Analyze the performance, security, and ethics (Bee benchmark) of the AI-generated projects. Focus on "Enterprise" constraints using benchmarks like Beaver. (Weeks 11-12).

### **8.2 The Evolution of the "Developer" Identity**

The identity of the software developer is shifting from "writer" to "editor" and "orchestrator." This does not mean the end of the profession, but its elevation. The "Vibe Coder" of the future will need:

* **Taste:** The aesthetic and functional judgment to know *what* to build.  
* **Literacy:** The technical literacy to know *when* the AI is lying.  
* **Ethics:** The moral compass to use benchmarks like **Bee** to ensure their creations are fair and equitable.

In conclusion, the integration of tools like Manus, technologies like Vibe Coding, and methods like PRIMM represents a renaissance in computer science education. By embracing these changes, we can cultivate a generation of technologists who are not merely subservient to machines, but who are masters of the new "English" of computation—empowered to create, verify, and lead in the age of Agentic AI.

## **9\. Appendix: Technical Comparison of Benchmarks**

**Table 2: The "Beacvhmarch" Landscape**

| Benchmark | SWE-bench (Verified) | BigCodeBench | Beaver | Bee (FHIBE) |
| :---- | :---- | :---- | :---- | :---- |
| **Primary Focus** | Software Engineering (Bug Fixing) | "Gluing" Libraries & Instruction Following | Enterprise Text-to-SQL | Fairness & Ethics in Computer Vision |
| **Data Source** | Real GitHub Issues (Django, etc.) | Diverse Library Calls (139 libs) | Private Enterprise Data Warehouses | Consensual Images of 2,000+ Participants |
| **Key Metric** | % of Issues Resolved (Pass/Fail) | Function Execution Success | SQL Accuracy on Complex Joins | Bias Metrics across Demographics |
| **Top Performer (2025)** | \~40-70% (Claude 3.5 / GPT-4o) | \~35-40% (Claude 3.5 Sonnet) | Significantly lower than public benchmarks | N/A (Used for Auditing) |
| **Educational Use** | "Can you fix what the AI couldn't?" | "Can you orchestrate complex libraries?" | "Can you handle messy enterprise data?" | "Is your model fair and unbiased?" |

This table summarizes the diverse evaluation metrics that define the modern AI landscape, providing a clear reference for educators and technical leaders to select the right tool for the right assessment.

#### **Referências citadas**

1. Vibe Coding Explained: Tools and Guides | Google Cloud, acessado em dezembro 4, 2025, [https://cloud.google.com/discover/what-is-vibe-coding](https://cloud.google.com/discover/what-is-vibe-coding)  
2. Not all AI-assisted programming is vibe coding (but vibe coding rocks), acessado em dezembro 4, 2025, [https://simonwillison.net/2025/Mar/19/vibe-coding/](https://simonwillison.net/2025/Mar/19/vibe-coding/)  
3. Vibe coding \- Wikipedia, acessado em dezembro 4, 2025, [https://en.wikipedia.org/wiki/Vibe\_coding](https://en.wikipedia.org/wiki/Vibe_coding)  
4. What is Vibe Coding? | IBM, acessado em dezembro 4, 2025, [https://www.ibm.com/think/topics/vibe-coding](https://www.ibm.com/think/topics/vibe-coding)  
5. What is vibe coding? | AI coding \- Cloudflare, acessado em dezembro 4, 2025, [https://www.cloudflare.com/learning/ai/ai-vibe-coding/](https://www.cloudflare.com/learning/ai/ai-vibe-coding/)  
6. Google CEO Sundar Pichai on how vibe Coding can help non-tech graduates build careers in technology, acessado em dezembro 4, 2025, [https://timesofindia.indiatimes.com/technology/tech-news/google-ceo-sundar-pichai-on-how-vibe-coding-can-help-non-tech-graduates-build-careers-in-technology/articleshow/125631791.cms](https://timesofindia.indiatimes.com/technology/tech-news/google-ceo-sundar-pichai-on-how-vibe-coding-can-help-non-tech-graduates-build-careers-in-technology/articleshow/125631791.cms)  
7. "Vibe Coding" has now infiltrated college classes : r/learnprogramming \- Reddit, acessado em dezembro 4, 2025, [https://www.reddit.com/r/learnprogramming/comments/1n5j3y0/vibe\_coding\_has\_now\_infiltrated\_college\_classes/](https://www.reddit.com/r/learnprogramming/comments/1n5j3y0/vibe_coding_has_now_infiltrated_college_classes/)  
8. Manus: Hands On AI, acessado em dezembro 4, 2025, [https://manus.im/](https://manus.im/)  
9. Wide Research \- Manus Documentation, acessado em dezembro 4, 2025, [https://manus.im/docs/features/wide-research](https://manus.im/docs/features/wide-research)  
10. Wide Research: Beyond Context Window \- Manus, acessado em dezembro 4, 2025, [https://manus.im/features/wide-research](https://manus.im/features/wide-research)  
11. What Developers Need to Know About Manus AI and Autonomous Coding, acessado em dezembro 4, 2025, [https://www.developernation.net/blog/what-developers-need-to-know-about-manus-ai-and-autonomous-coding/](https://www.developernation.net/blog/what-developers-need-to-know-about-manus-ai-and-autonomous-coding/)  
12. How Heicoders Students Are Using Manus AI to Solve Real Problems, acessado em dezembro 4, 2025, [https://heicodersacademy.com/blog/how-heicoders-students-are-using-manus-ai-to-solve-real-problems/](https://heicodersacademy.com/blog/how-heicoders-students-are-using-manus-ai-to-solve-real-problems/)  
13. Manus AI Use Cases & Real-World Applications \- Single Grain, acessado em dezembro 4, 2025, [https://www.singlegrain.com/marketing/manus-ai-use-cases-real-world-applications/](https://www.singlegrain.com/marketing/manus-ai-use-cases-real-world-applications/)  
14. Cursor vs. Manus AI Comparison \- SourceForge, acessado em dezembro 4, 2025, [https://sourceforge.net/software/compare/Cursor-vs-Manus/](https://sourceforge.net/software/compare/Cursor-vs-Manus/)  
15. Vibe coding a full fledged retro dungeon crawler game in Cursor \- Reddit, acessado em dezembro 4, 2025, [https://www.reddit.com/r/cursor/comments/1jo36zx/vibe\_coding\_a\_full\_fledged\_retro\_dungeon\_crawler/](https://www.reddit.com/r/cursor/comments/1jo36zx/vibe_coding_a_full_fledged_retro_dungeon_crawler/)  
16. Top Agentic IDEs Reviewed: Cursor AI, Windsurf, Void, and Aide, acessado em dezembro 4, 2025, [https://aiagentsdirectory.com/blog/top-agentic-ides-comprehensive-reviews-of-ai-powered-development-tools](https://aiagentsdirectory.com/blog/top-agentic-ides-comprehensive-reviews-of-ai-powered-development-tools)  
17. You're Vibe Coding Wrong, acessado em dezembro 4, 2025, [https://alliance.xyz/essays/youre-vibe-coding-wrong](https://alliance.xyz/essays/youre-vibe-coding-wrong)  
18. Google NotebookLM | AI Research Tool & Thinking Partner, acessado em dezembro 4, 2025, [https://notebooklm.google/](https://notebooklm.google/)  
19. NotebookLM: AI-Powered Research and Learning Assistant Tool | Google Workspace, acessado em dezembro 4, 2025, [https://workspace.google.com/products/notebooklm/](https://workspace.google.com/products/notebooklm/)  
20. NotebookLM for enterprise \- Google Cloud, acessado em dezembro 4, 2025, [https://cloud.google.com/resources/notebooklm-enterprise](https://cloud.google.com/resources/notebooklm-enterprise)  
21. Best AI Coding Models for Software Development 2025: Performance, Cost, and Future Outlook, acessado em dezembro 4, 2025, [https://lunabase.ai/blog/best-ai-coding-models-for-software-development-2025-performance-cost-and-future-outlook](https://lunabase.ai/blog/best-ai-coding-models-for-software-development-2025-performance-cost-and-future-outlook)  
22. Introducing SWE-bench Verified \- OpenAI, acessado em dezembro 4, 2025, [https://openai.com/index/introducing-swe-bench-verified/](https://openai.com/index/introducing-swe-bench-verified/)  
23. SWE-bench Leaderboards, acessado em dezembro 4, 2025, [https://www.swebench.com/](https://www.swebench.com/)  
24. Demystifying LLM Leaderboards: What You Need to Know \- Shakudo, acessado em dezembro 4, 2025, [https://www.shakudo.io/blog/demystifying-llm-leaderboards-what-you-need-to-know](https://www.shakudo.io/blog/demystifying-llm-leaderboards-what-you-need-to-know)  
25. BEAVER: An Enterprise Benchmark for Text-to-SQL \- Peter Baile Chen, acessado em dezembro 4, 2025, [https://peterbaile.github.io/beaver/](https://peterbaile.github.io/beaver/)  
26. BEAVER: An Enterprise Benchmark for Text-to-SQL, acessado em dezembro 4, 2025, [https://powerdrill.ai/discover/discover-BEAVER-An-Enterprise-cm0prw4f21033014h7gsugw0r](https://powerdrill.ai/discover/discover-BEAVER-An-Enterprise-cm0prw4f21033014h7gsugw0r)  
27. BEAVER: An Enterprise Benchmark for Text-to-SQL \- arXiv, acessado em dezembro 4, 2025, [https://arxiv.org/html/2409.02038v1](https://arxiv.org/html/2409.02038v1)  
28. Sony Debuts Benchmark for Measuring Computer Vision Bias \- \- ETCentric, acessado em dezembro 4, 2025, [https://www.etcentric.org/sony-debuts-benchmark-for-measuring-computer-vision-bias/](https://www.etcentric.org/sony-debuts-benchmark-for-measuring-computer-vision-bias/)  
29. Sony AI releases benchmark testing database for computer vision fairness testing, acessado em dezembro 4, 2025, [https://www.biometricupdate.com/202511/sony-ai-releases-benchmark-testing-database-for-computer-vision-fairness-testing](https://www.biometricupdate.com/202511/sony-ai-releases-benchmark-testing-database-for-computer-vision-fairness-testing)  
30. Best Vibe Coding Courses & Certificates \[2026\] \- Coursera, acessado em dezembro 4, 2025, [https://www.coursera.org/courses?query=vibe%20coding](https://www.coursera.org/courses?query=vibe+coding)  
31. MicroSims: A Framework for AI-Generated, Scalable Educational Simulations with Universal Embedding and Adaptive Learning Support \- arXiv, acessado em dezembro 4, 2025, [https://arxiv.org/html/2511.19864v1](https://arxiv.org/html/2511.19864v1)  
32. acessado em dezembro 4, 2025, [https://www.researchgate.net/publication/384575501\_PRIMM\_in\_Constructivist\_Classroom\_Enhancing\_Programming\_Education\_through\_Active\_Learning\#:\~:text=In%20this%20paper%20we%20describe%20an%20approach%20to%20teaching%20programming,tracing%20and%20code%20comprehension%20research.](https://www.researchgate.net/publication/384575501_PRIMM_in_Constructivist_Classroom_Enhancing_Programming_Education_through_Active_Learning#:~:text=In%20this%20paper%20we%20describe%20an%20approach%20to%20teaching%20programming,tracing%20and%20code%20comprehension%20research.)  
33. Using generative AI in the classroom A guide for computing teachers, acessado em dezembro 4, 2025, [https://computingeducationresearch.org/wp-content/uploads/2024/07/AICT-Guidance.pdf](https://computingeducationresearch.org/wp-content/uploads/2024/07/AICT-Guidance.pdf)  
34. How To Use NotebookLM As A Developer? \- A Comprehensive Guide \- JavaTechOnline, acessado em dezembro 4, 2025, [https://javatechonline.com/how-to-use-notebooklm-as-a-developer/](https://javatechonline.com/how-to-use-notebooklm-as-a-developer/)  
35. What is Vibe Coding? How To Vibe Your App to Life \- Replit Blog, acessado em dezembro 4, 2025, [https://blog.replit.com/what-is-vibe-coding](https://blog.replit.com/what-is-vibe-coding)  
36. Gamification Powered by a Large Language Model to Enhance Flipped Classroom Learning in Undergraduate Computer Science, acessado em dezembro 4, 2025, [https://papers.academic-conferences.org/index.php/ecgbl/article/download/2630/2565/10435](https://papers.academic-conferences.org/index.php/ecgbl/article/download/2630/2565/10435)  
37. Large Language Model-Driven Classroom Flipping: Empowering Student-Centric Peer Questioning with Flipped Interaction \- arXiv, acessado em dezembro 4, 2025, [https://arxiv.org/html/2311.14708](https://arxiv.org/html/2311.14708)  
38. Personalized Parsons Puzzles as Scaffolding Enhance Practice Engagement Over Just Showing LLM-Powered Solutions \- arXiv, acessado em dezembro 4, 2025, [https://arxiv.org/html/2501.09210v1](https://arxiv.org/html/2501.09210v1)  
39. Automating Personalized Parsons Problems with Customized Contexts and Concepts, acessado em dezembro 4, 2025, [https://arxiv.org/html/2404.10990v1](https://arxiv.org/html/2404.10990v1)  
40. Vibe Coding: How AI is Transforming the MBA Experience at Yale, acessado em dezembro 4, 2025, [https://som.yale.edu/story/2025/vibe-coding-how-ai-transforming-mba-experience-yale](https://som.yale.edu/story/2025/vibe-coding-how-ai-transforming-mba-experience-yale)  
41. Context Engineering for AI Agents: Lessons from Building Manus, acessado em dezembro 4, 2025, [https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)  
42. Aprendizagem de programação por pares IA-Humano: Explorando o Potencial do ChatGPT para a aprendizagem de Programação \- UFPel Institucional \- Universidade Federal de Pelotas, acessado em dezembro 4, 2025, [https://institucional.ufpel.edu.br/projetos/id/u7415](https://institucional.ufpel.edu.br/projetos/id/u7415)