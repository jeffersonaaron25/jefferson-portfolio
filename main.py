from fasthtml.common import *
import asyncio
import styles
from components import *
import llm

global_style = styles.global_style
app = FastHTML(hdrs=(global_style,), ws_hdr=True)

@app.route('/')
def get():
    return Body(
        Terminal(),
    )

async def stream_characters(text, send, element_id):
    index = 0
    while index < len(text):
        await send(Div(text[:index + 1], hx_swap_oob='innerHTML', id=element_id))
        index += 1
        await asyncio.sleep(0.02)


async def Intro(send):
    intro_message = [
        "Welcome to my portfolio! My name is Jefferson.",
        "I am a software engineer skilled in Python, Cloud (GCP, AWS), LLMs and more.",
        "I also have some experience with frontend technologies like React, React Native and TypeScript, and databases like PostgreSQL, Firestore, MySQL and Redis.",
        "Over the years, i have learned a lot other various tools as needed for the projects I have worked on.",
        "In this terminal, you can type commands to learn more about me.",
        "Type 'help' for available commands.",
        "You can also type anything you want to know about me, and JeffAI (a rag based LLM) will try to answer you.",
        "Let's get started!"
    ]
    for i,message in enumerate(intro_message):
        await stream_characters(message, send, 'intro_ln'+str(i+1))
        await asyncio.sleep(0)
 
    await send(
            Form(
                TerminalInput(),
                id='form',
                hx_ext="ws", ws_connect="/ws", ws_send=""
            ),
        )

async def on_connect(send):  await Intro(send)

@app.ws('/wsintro', conn=on_connect)
async def ws_intro(send):
    return

@app.ws('/ws', name='ws')
async def ws(input: str, send):    
    responses = {
        'help': 'Available commands: about, contact, education, experience, projects, skills. You can also type anything you want to know about me, and JeffAI (a rag based LLM) will try to answer you.',
        'about': 'I am a software engineer with a passion for python development.',
        'contact': 'Contact me at +1 (347) 957 5717 or ja4568@nyu.edu.',
        'education': 'I studied computer engineering at New York University.',
        'experience': 'I started a tech company when I was 19, before I moved to New York to pursue higher education. Recently, I also did my internship as a data engineer at Swiss Re.',
        'projects': 'I have worked on various projects, including a chatbot, a web scraper, and a data visualization tool.',
        'skills': 'I am proficient in Python, JavaScript, and SQL.',
    }
    await send(
            TerminalInput(
                id="input-container",
                hidden=True
            )
        )
    # Print input command
    await send(Div(TerminalMessage(input, id="none", prefix=True), hx_swap_oob='beforeend', id="terminal-list"))
    # Get the response for the command
    response = responses.get(input, None)

    if response is None:
        # Print loader
        await send(Div(TerminalMessage("JeffAI is typing", id="none"), hx_swap_oob='beforeend', id="terminal-list"))
        response = await llm.get_llm_response(input)

    # Print response
    await send(Div(TerminalMessage(response, id="none"), hx_swap_oob='beforeend', id="terminal-list"))

    await send(
            TerminalInput(
                id="input-container",
                hidden=False
            )
        )

serve()
