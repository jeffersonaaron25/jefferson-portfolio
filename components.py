from fasthtml.common import *
# Terminal message component
def TerminalMessage(text, id, prefix=False):
    return Div(
            Span("user@browser %", cls="output", style="font-weight: bold; color: #ffbd2e;") if prefix else Span(">", style="color: #27c93f; font-weight: bold;", cls="output"),
            Span(text, cls="output", id=id),
            cls="terminal-line", hx_swap_oob='innerHTML'
        )

# The input field for the terminal command
def TerminalInput(id="input-container", hidden=False):
    return Div(
        Span("user@browser %", cls="output", style="font-weight: bold; color: #ffbd2e;"),
        
        Input(
            # Span("_", cls="blinking-cursor"),
            type="text", name='input', id='input', 
            placeholder="", 
            cls="terminal-input", hx_swap_oob='true',
            autofocus=True,
            # style="caret-color: transparent;"
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
