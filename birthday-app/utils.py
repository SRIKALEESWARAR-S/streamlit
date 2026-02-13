import random
from poems import poems

def generate_poem(language,relation,name):
    try:
        selected = random.choice(poems[language][relation])
        return selected.format(name=name)
    except KeyError:
        return "invalid selection"
    
    
