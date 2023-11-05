import blessed

t = blessed.Terminal()

templates = {
    "info": f"{t.blue}[i] MSG",
    "success": f"{t.green}MSG",
    "error": f"{t.red}ERROR: MSG"
}

def msg(msg, level):
    print(templates[level].replace("MSG", msg), t.normal)