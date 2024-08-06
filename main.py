from fasthtml.common import *
import asyncio
import styles
from components import *
from starlette.middleware.cors import CORSMiddleware

import llm

global_style = styles.global_style
app = FastHTML(hdrs=(global_style,), ws_hdr=True)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
    allow_origins=['*'],
)

@app.route('/')
def get():
    return Title(
            "Jefferson Nelsson's Portfolio"
            ), Link(
            rel="icon", type="image/png", href="https://img.icons8.com/?size=100&id=lURRtQpmUhiT&format=png&color=000000"
        ), Body(Terminal(), FooterLinks())

async def stream_characters(text, send, element_id):
    index = 0
    while index < len(text):
        await send(Div(text[:index + 1], hx_swap_oob='innerHTML', id=element_id))
        index += 1
        await asyncio.sleep(0.02)


async def Intro(send):
    try:
        intro_message = [
            "Welcome to my portfolio! My name is Jefferson.",
            "I am a software engineer skilled in Python, Cloud (GCP, AWS), LLMs and more.",
            "I have also gained experience with frontend technologies such as React, React Native, and TypeScript, as well as databases like PostgreSQL, Firestore, MySQL, and Redis.",
            "Throughout my career, I have continuously learned and adapted to various tools and technologies as required for the projects I have worked on.",
            "In this terminal, you can type commands to learn more about me.",
            "Type 'help' for available commands.",
            "You can also type anything you want to know about me, and JeffAI (a rag based LLM) will try to answer you.",
            "Let's get started!"
        ]
        for i,message in enumerate(intro_message):
            await stream_characters(message, send, 'intro_ln'+str(i+1))
            await asyncio.sleep(1)
    
        await send(
                Form(
                    TerminalInput(),
                    id='form',
                    hx_ext="ws", ws_connect="/ws", ws_send=""
                ),
            )
    except Exception as e:
        print(e)

async def on_connect(send):  await Intro(send)

@app.ws('/wsintro', conn=on_connect)
async def ws_intro(send):
    return

@app.ws('/ws', name='ws')
async def ws(input: str, send):    
    responses = {
        'help': 'Available commands: about, contact, education, experience, projects, skills. You can also type anything you want to know about me, and JeffAI (a rag based LLM) will try to answer you.',
        'about': 'I am a software engineer with a passion for python development.',
        'contact': 'Contact me at +1 (347) 957 5717 or jefferson.nelsson@nyu.edu.',
        'education': 'I got my Master\'s degree in Computer Science from New York University. My coursework focused on software engineering and machine learning.',
        'experience': 'I started a tech company when I was 19, before I moved to New York to pursue higher education. Recently, I also did my internship as a data engineer at Swiss Re.',
        'projects': 'I have worked on various projects, including a PySpark chatbot called SparkLLM which can perform operations on datasets, a job prediction system as part of my Deep Learning course at NYU, a web app to extract email and convert them into tickets for customer support, and more personal projects in Python, Java, React and LLM technologies.',
        'skills': 'I am proficient in Python, LLMs, Google Cloud Platform, React JS, and SQL.',
        '': 'Please type a command. Type "help" for available commands.'
    }
    try:
        await send(
                TerminalInput(
                    hidden=True
                )
            )
        # Print input command
        await send(Div(TerminalMessage(input, prefix=True), hx_swap_oob='beforeend', id="terminal-list"))
        # Get the response for the command
        response = responses.get(input.lower().strip(), None)

        if response is None:
            # Print loader
            await send(Div(TerminalMessage("JeffAI is typing"), hx_swap_oob='beforeend', id="terminal-list"))
            response = await llm.get_llm_response(input)

        # Print response
        await send(Div(TerminalMessage(response), hx_swap_oob='beforeend', id="terminal-list"))

        await send(
                TerminalInput(
                    hidden=False
                )
            )
    except Exception as e:
        print(e)

# serve() # for local dev