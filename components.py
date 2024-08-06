from fasthtml.common import *

def FooterLinks():
    return Footer(
            P("Made with ❤️ by Jefferson"),
            Div(
                A(
                    Img(
                        src="https://img.icons8.com/?size=100&id=108812&format=png&color=ffffff",
                        alt="LinkedIn",
                    ),
                    href="https://www.linkedin.com/in/jeffersonaaron/",
                    target="_blank"
                ),
                A(
                    Img(
                        src="https://img.icons8.com/?size=100&id=118553&format=png&color=ffffff",
                        alt="GitHub",
                    ),
                    href="https://github.com/jeffersonaaron25",
                    target="_blank"
                ),
                A(
                    Img(
                        src="https://img.icons8.com/?size=100&id=108813&format=png&color=ffffff",
                        alt="Email",
                    ),
                    href="mailto:jefferson.nelsson@nyu.edu",
                ),
                A(
                    Img(
                        src="https://img.icons8.com/?size=100&id=sXhQ3VwDMMBx&format=png&color=000000",
                        alt="Phone",
                    ),
                    href="tel:+13479575717",
                ),
                cls="footer"
            )
        )

# Terminal message component
def TerminalMessage(text, prefix=False):
    return Div(
            Span("user@browser %", cls="output", style="font-weight: bold; color: #ffbd2e;") if prefix else Span(">", style="color: #27c93f; font-weight: bold;", cls="output"),
            Span(text, cls="output"),
            cls="terminal-line", hx_swap_oob='innerHTML'
        )

# The input field for the terminal command
def TerminalInput(id="input-container", hidden=False):
    return Div(
        Span("user@browser %", cls="output", style="font-weight: bold; color: #ffbd2e;"),
        
        Input(
            type="text", name='input', id='input', 
            placeholder="Type here...", 
            cls="terminal-input", hx_swap_oob='true',
            autofocus=True,
        ),
        id = id,
        style="display: none;" if hidden else "",
        cls="terminal-input-container",
    )


def IntroMessage(n):
    return Div(
        Span("user@browser %", style="font-weight: bold; color: #ffbd2e;", cls="output"),
        Span("Hello there!", cls="output"),
        Br(),
        *[Span(
            "",
            cls='output',
            id='intro_ln'+str(i+1),
        ) if i in [2, 3, 5, 6] else
        P(
            "",
            cls='output',
            id='intro_ln'+str(i+1),
        )
        for i in range(n)],
        hx_ext="ws", ws_connect="/wsintro", ws_send="", hx_swap_oob='innerHTML',
        cls="terminal-line",
    )

# Define the terminal component
def Terminal():
    return Div(
        Div(
            Div(
                Span(cls='close'),
                Span(cls='minimize'),
                Span(cls='maximize'),
                cls='buttons'
            ),
            Div("Jefferson Nelsson's Portfolio", cls='title'),
            cls='terminal-header'
        ),
        Div(
            IntroMessage(n=8),
            Div(id='terminal-list'),
            Div(
                id='form'
            ),
            cls='terminal-body',
        ),
        cls='terminal',
    )
