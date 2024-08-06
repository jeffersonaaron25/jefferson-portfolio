from fasthtml.common import Style

global_style = Style('''
body {
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Menlo', 'Monaco', 'Courier New', Courier, monospace;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

.terminal {
    background-color: #2d2d2d;
    border-radius: 5px;
    width: 80%;
    max-width: 800px;
    height: 500px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    margin-bottom: 20px;  /* Added margin for spacing */
}

.terminal-header {
    background-color: #3c3c3c;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

.title {
    color: #d4d4d4;
    font-size: 14px;
    text-align: center;
    font-weight: bold;
}

.terminal-body {
    padding: 20px;
    height: 420px;
    overflow-x: hidden;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #3c3c3c #2d2d2d;
}
                     
.terminal-body::-webkit-scrollbar {
    width: 8px;
}

.terminal-body::-webkit-scrollbar-track {
    background: #2d2d2d; /* Track color */
}

.terminal-body::-webkit-scrollbar-thumb {
    background-color: #3c3c3c; /* Thumb color */
    border-radius: 10px; /* Optional: round the corners */
    border: 2px solid #2d2d2d; /* Optional: add a border */
}
.output {
    margin-bottom: 10px;
    font-size: 14px;
    line-height: 1.5;
}


.buttons {
    display: flex;
    gap: 5px;
}

.buttons span {
    display: block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.buttons .close {
    background-color: #ff5f56;
}

.terminal-line {
    align-items: center;
    padding: 4px 0;
    font-size: 14px;
}

.buttons .minimize {
    background-color: #ffbd2e;
}

.buttons .maximize {
    background-color: #27c93f;
}
                     
.terminal-input-container {
    display: flex;
    align-items: center;
    padding: 4px 0;
    font-size: 14px;
}

.terminal-input {
    background-color: transparent;
    color: #d4d4d4;
    border: 0px solid #2d2d2d;
    outline: none;
    font-family: 'Menlo', 'Monaco', 'Courier New', Courier, monospace;
    font-size: 14px;
    width: 42vw;
    margin-left: 5px;
    margin-bottom: 10px;
}

.footer {
    text-align: center;
    margin-top: 20px;
    color: #d4d4d4;
    font-size: 14px;
}
.footer img {
    width: 40px;
    height: 40px;
    margin: 0 0px;
    vertical-align: middle;
}
.footer a {
    color: #d4d4d4;
    text-decoration: none;
    margin: 0 5px;
}

::placeholder {
    color: transparent;
}              
                     
@media (max-width: 480px) {
    .terminal {
        width: 90%;
    }
    .terminal-input {
        width: 48vw;
        font-size: 12px;
    }
    .output {
        font-size: 12px;
    }
    .terminal-input-container {
        font-size: 12px;
    }
    .title {
        font-size: 12px;
    }
    .terminal-line {
        font-size: 12px;
    }
    .footer {
        font-size: 12px;
    }
    body {
        overflow: hidden;
        height: 90vh;
    }
    ::placeholder {
        color: #d4d4d4;
    }
}

@media (max-width: 400px) {
    .terminal {
        width: 90%;
    }
    .terminal-input {
        width: 44vw;
        font-size: 10px;
    }
    .output {
        font-size: 10px;
    }
    .terminal-input-container {
        font-size: 10px;
    }
    .title {
        font-size: 10px;
    }
    .terminal-line {
        font-size: 10px;
    }
    .footer {
        font-size: 10px;
    }
    body {
        overflow: hidden;
        height: 90vh;
    }        
    ::placeholder {
        color: #d4d4d4;
    }
}
''')