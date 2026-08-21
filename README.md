ShopAI — Agentic Commerce Assistant
---
ShopAI is a lightweight, autonomous e-commerce agent and storefront backend built with FastAPI and Python. The system provides an interactive web storefront where users can authenticate, browse catalog items, and interact with a tool-calling shopping agent that searches inventory and manages user carts.FeaturesAutonomous Commerce Agent: Natural language processing agent capable of inspecting catalog data, querying product availability, and managing carts.FastAPI Backend: High-performance asynchronous REST API handling chat workflows and static assets.Embedded Database: SQLite integration with automated startup migration and product catalog seeding.Modern Storefront UI: Clean, responsive web interface built with Tailwind CSS, including an interactive chat drawer and client-side session management.Cloud-Ready: Pre-configured deployment scripts for platforms like Render using ASGI/Uvicorn.Repository StructurePlaintextai-commerce-agent/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI server, lifespan events, and routing
│   ├── agent.py             # Agent runtime and tool orchestration
│   ├── tools.py             # Business logic tools (Search, Cart, Stock)
│   ├── models.py            # Pydantic schemas for validation
│   └── database.py          # SQLite database connection and seeding
├── static/
│   └── index.html           # Storefront frontend and chat interface
├── .gitignore               # Ignored environments, databases, and caches
├── .env.example             # Template for local environment variables
├── requirements.txt         # Project dependencies
├── render.yaml              # Render blueprint deployment file
└── README.md                # Project documentation
PrerequisitesPython 3.10 or higherGitLocal SetupClone the repository:Bashgit clone https://github.com/<YOUR_USERNAME>/ai-commerce-agent.git
cd ai-commerce-agent
Create and activate a virtual environment:Linux/macOS:Bashpython3 -m venv venv
source venv/bin/activate
Windows:Bashpython -m venv venv
venv\Scripts\activate
Install dependencies:Bashpip install -r requirements.txt
Set up environment variables:Bashcp .env.example .env
(Optional) Configure API credentials in .env if integrating third-party LLM providers.Run the local development server:Bashuvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
Access the application:Storefront UI: [http://127.0.0.1:8000](http://127.0.0.1:8000)Interactive API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)Deployment on RenderThis service is configured for direct deployment on Render via Web Services.Deployment ConfigurationRuntime: Python 3Root Directory: (Leave blank)Build Command: pip install -r requirements.txtStart Command: uvicorn app.main:app --host 0.0.0.0 --port $PORTEnvironment VariablesVariableRequiredDescriptionPORTAuto-setPort assigned dynamically by RenderPYTHON_VERSIONOptionalSpecifies runtime version (e.g., 3.11.0)OPENAI_API_KEY / GEMINI_API_KEYOptionalRequired only if running live LLM integrationsAPI ReferenceHealth CheckEndpoint: GET /Description: Serves the static single-page storefront.Agent Chat EndpointEndpoint: POST /chatHeaders: Content-Type: application/jsonRequest Body:JSON{
  "message": "Find headphones under $150",
  "session_id": "user_123"
}
Response Body:JSON{
  "response": "Found items: [{'id': 'prod_1', 'name': 'Wireless Noise-Canceling Headphones', 'price': 149.99, 'stock': 15}]",
  "session_id": "user_123"
}
Frontend -> https://shopmate-ai-agentic-commerce.onrender.com
Backend ->  https://shopmate-ai-agentic-commerce.onrender.com/docs
