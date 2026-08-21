ShopAI — Agentic Commerce Assistant
--
ShopAI is a lightweight, autonomous e-commerce agent and storefront backend built with FastAPI and Python. The system provides an interactive web storefront where users can authenticate, browse catalog items, and interact with a tool-calling shopping agent that searches inventory and manages user carts.

Features
--
Autonomous Commerce Agent: Natural language processing agent capable of inspecting catalog data, querying product availability, and managing carts.

1.FastAPI Backend: High-performance asynchronous REST API handling chat workflows and static assets.

2.Embedded Database: SQLite integration with automated startup migration and product catalog seeding.

3.Modern Storefront UI: Clean, responsive web interface built with Tailwind CSS, including an interactive chat drawer and client-side session management.

Repository Structure
---
ai-commerce-agent/
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

Local Setup
--
1.Clone the repository:
git clone https://github.com/KashishVishwakarma/shopmate-ai-agentic-commerce
cd ai-commerce-agent
2.Create and activate a virtual environment:

Linux/macOS:
python3 -m venv venv
source venv/bin/activate
Windows:
python -m venv venv
venv\Scripts\activate
Cloud-Ready: Pre-configured deployment scripts for platforms like Render using ASGI/Uvicorn

Live 
---
Frontend -> https://shopmate-ai-agentic-commerce.onrender.com

Backend ->  https://shopmate-ai-agentic-commerce.onrender.com/docs
