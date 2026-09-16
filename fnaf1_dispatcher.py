import sys
import subprocess
import re

# ANSI Color Codes for Termux
COLOR_RESET = "\033[0m"
COLOR_PURPLE = "\033[35m"  # Bonnie
COLOR_BROWN = "\033[33m"   # Freddy / Golden Freddy
COLOR_YELLOW = "\033[93m"  # Chica
COLOR_RED = "\033[31m"     # Foxy

# FNaF 1 Hard Data, Intervals, Lore, and Easter Eggs Database
FNAF1_DATABASE = {
    "1": {
        "title": "Night 1: The Foundation & Phone Guy's Warning",
        "ai_intervals": "Bonnie & Chica check every 4.97 sec (Threshold increases as night progresses). Freddy & Foxy: Inactive (Foxy is dormant, Freddy stays on stage).",
        "mechanics": "You have generous power. Bonnie starts moving around 2 AM (+1 AI). Doors can be held longer, but don't make a habit of it.",
        "lore": "Establishes the 'Bite of '87' context. Phone Guy mentions the animatronics can walk around during the day 'before the bite', and that human beings can only live without frontal lobes.",
        "easter_eggs": "Check CAM 1A (Show Stage)—the posters of Freddy can randomly change into terrifying close-ups of crying children or 'IT'S ME' hallucinations."
    },
    "2": {
        "title": "Night 2: Enter Foxy",
        "ai_intervals": "Foxy activates. Every time you lower the monitor, Foxy rolls a cooldown between 0.5s to 10.5s before rushing. Bonnie and Chica get hyper-aggressive.",
        "mechanics": "Foxy mechanics: Checking CAM 1C (Pirate Cove) freezes him, but staring at him too much drains your time, and ignoring him lets him run down the West Hall (listen for footsteps, slam the left door).",
        "lore": "The restaurant's dark past deepens. Phone Guy hints at the previous employees and bodies being stuffed into suits ('smell like reanimated corpses').",
        "easter_eggs": "The West Hall poster can change to show 'IT'S ME' or pictures of the crying children folding their heads back."
    },
    "3": {
        "title": "Night 3: Freddy Comes Alive",
        "ai_intervals": "Freddy rolls a movement check every 3.02 seconds against his AI level. Foxy's speed increases drastically.",
        "mechanics": "Freddy's Loop: He moves Cam 1A -> 1B -> 7 (Restrooms) -> 6 (Kitchen) -> 4A -> 4B. Staring at Freddy on the monitor freezes his movement countdown, but if he reaches the East Hall Corner (Cam 4B), looking at him actually stops him from entering unless you look away with the right door open.",
        "lore": "The realization that the animatronics view you not as a guest, but as an endoskeleton without a costume, meaning they need to forcefully stuff you into a metal suit.",
        "easter_eggs": "Kitchen Camera (CAM 6) has no visual feed—only audio. If you listen closely during Freddy's song, you hear the Toreador March music box."
    },
    "4": {
        "title": "Night 4: Phone Guy's Demise",
        "ai_intervals": "AI levels spike across the board. Bonnie and Chica cycle aggressively every 4.97 seconds.",
        "mechanics": "Resource management is razor-thin. You must balance camera flips to stall Foxy with light-checking the doors. Heavy reliance on audio cues (groans in the hall mean back away from the monitor and check lights).",
        "lore": "Phone Guy's final call. You hear him get attacked, a heavy thump, and the golden Freddy suit groan/jumpscare sound at the end of the transmission.",
        "easter_eggs": "The backstage camera (CAM 5) can occasionally show all spare animatronic heads staring directly into the camera lens, tracking the player."
    },
    "5": {
        "title": "Night 5: The Supernatural Phase",
        "ai_intervals": "High AI levels. Animatronics move almost every check cycle. Freddy starts moving actively from the start.",
        "mechanics": "Golden Freddy can now appear randomly in your office if you look at CAM 2B and the poster switches to a close-up of his face. You must quickly pull the monitor back up to survive.",
        "lore": "Messages on the phone turn into garbled, demonic/retro-sounding audio tracks (backwards voice clips talking about the origin of the murders).",
        "easter_eggs": "The newspaper clippings in East Hall change text dynamically between nights, detailing the missing children incidents and the health code violations of the restaurant."
    },
    "6": {
        "title": "Night 6 & 4/20 Mode: Maximum Chaos",
        "ai_intervals": "All animatronics locked to AI 20. Movement checks succeed almost instantly.",
        "mechanics": "The ultimate test of muscle memory. Never open cameras except a quick flash to CAM 1C to keep Foxy back. Listen strictly to audio cues, manage power down to the exact percentage, and lock down the doors.",
        "lore": "Completing this night rewards you with a 'Overtime' bonus check and unlocks the custom night where you can freely input custom AI values.",
        "easter_eggs": "Setting the Custom Night AI to 1/9/8/7 triggers Golden Freddy's jumpscare instantly, crashing the game straight to the desktop."
    }
}

# ASCII Art Library
ASCII_ART = {
    "1": f"""{COLOR_PURPLE}
    /\_/\
   ( o.o )  [ BONNIE THE BUNNY ]
    > ^ <
   /|   |\
  (_|___|_)
{COLOR_RESET}""",
    "2": f"""{COLOR_BROWN}
     ___
    /o o\   [ FREDDY FAZBEAR ]
   (  =  )
   /|   |\
  (_|___|_)
{COLOR_RESET}""",
    "3": f"""{COLOR_YELLOW}
    (o>
    ///\    [ CHICA THE CHICKEN ]
   (____)
    || ||
{COLOR_RESET}""",
    "4": f"""{COLOR_RED}
    |\_/|
    |o.o|   [ FOXY THE PIRATE ]
   (  V  )
   /|   |\
  (_|___|_)
{COLOR_RESET}""",
    "5": f"""{COLOR_YELLOW}
     ___
    /x x\   [ GOLDEN FREDDY ]
   (  =  )
   /|   |\  * IT'S ME *
  (_|___|_)
{COLOR_RESET}"""
}

HARD_CODED_STRATEGIES = {
    r"how (to|do i) (beat|stop|counter) chica": "Chica approaches from the East (Right) door. Toggle your right door light to spot her window silhouette. If you hear window groans or kitchen pots clattering, shut the right door immediately.",
    r"how (to|do i) (beat|stop|counter) bonnie": "Bonnie approaches from the West (Left) door. Check your left door light frequently. If he appears in the blindspot, shut the left door until he leaves.",
    r"how (to|do i) (beat|stop|counter) foxy": "Foxy stays in Pirate Cove (CAM 1C). Check CAM 1C periodically to delay his sprint. If he leaves the cove, immediately shut your West (Left) door before checking CAM 2A.",
    r"how (to|do i) (beat|stop|counter) freddy": "Freddy moves along the right side (CAM 1A -> 1B -> 7 -> 6 -> 4A -> 4B). Staring at him on the monitor freezes his movement countdown. Keep your camera focused on CAM 4B when he is close.",
    r"power|usage|drain": "Power drains based on active usage bars (1 to 5 bars). 1 bar (passive office) consumes 1% power every 9.6 seconds. Each added active component (Monitor, Door Light, Closed Door) adds 1 usage bar, accelerating the drain tick.",
}

FAKE_CONCEPTS = [
    "pizza", "eat", "eating", "sparky", "phone guy alive", 
    "cupcake jumpscare", "kitchen visual", "honk nose death",
    "yellow dog", "dog animatronic", "secret animatronic", "back room"
]

def query_ollama(user_question, night_data):
    lower_q = user_question.lower()
    
    for pattern, response in HARD_CODED_STRATEGIES.items():
        if re.search(pattern, lower_q):
            return f"[LOCAL OVERRIDE]: {response}"
            
    if any(fake in lower_q for fake in FAKE_CONCEPTS):
        return "[ENGINE REJECTION]: Query references non-existent game code, hoaxes, or fake fan mechanics."

    system_framing = (
        "You are an exact numerical UI mechanic guide for Five Nights at Freddy's 1. "
        "Answer the user's question directly in 1-2 sentences using ONLY real FNaF 1 game mechanics. "
        "Do not invent fake code, variables, or secret rooms. State facts directly without listing hypothetical examples."
    )
    
    full_prompt = f"{system_framing}\n\nQuestion: {user_question}\nAnswer:"
    
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:1b", full_prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[Error connecting to Ollama: {e}]"

def render_art_menu():
    while True:
        print("\n" + "="*30)
        print("     FNAF ART GALLERY     ")
        print("="*30)
        print("1. Bonnie")
        print("2. Freddy")
        print("3. Chica")
        print("4. Foxy")
        print("5. Golden Freddy")
        print("b. Back to Main Menu")
        
        art_choice = input("\nSelect character: ").strip().lower()
        if art_choice == 'b':
            break
        elif art_choice in ASCII_ART:
            print(ASCII_ART[art_choice])
        else:
            print("Invalid character option.")

def main():
    while True:
        print("\n" + "="*50)
        print(" FNAF 1: HARDCORE DISPATCHER & LORE ENGINE ")
        print("="*50)
        print("Select Night / Scenario:")
        for key, data in FNAF1_DATABASE.items():
            print(f"{key}. {data['title']}")
        print("7. FNaF Art")
        print("q. Quit")
        
        choice = input("\nSelect option: ").strip().lower()
        if choice == 'q':
            sys.exit(0)
        elif choice == '7':
            render_art_menu()
        elif choice in FNAF1_DATABASE:
            night_loop(FNAF1_DATABASE[choice])
        else:
            print("Invalid selection, night guard.")

def night_loop(night_data):
    while True:
        print(f"\n--- {night_data['title']} ---")
        print("1. View Exact AI Intervals & Movement Math")
        print("2. View Survival Mechanics & Strategy")
        print("3. View Lore Deep-Dive & Phone Guy Secrets")
        print("4. View Hidden Easter Eggs & Glitches (e.g., 1987)")
        print("5. Ask AI Dispatcher a Custom Question")
        print("b. Back to Night Selection")
        
        action = input("\nSelect diagnostic mode: ").strip().lower()
        
        if action == 'b':
            break
        elif action == '1':
            print(f"\n[AI TIMINGS & INTERVALS]:\n{night_data['ai_intervals']}")
        elif action == '2':
            print(f"\n[SURVIVAL MECHANICS]:\n{night_data['mechanics']}")
        elif action == '3':
            print(f"\n[LORE DEEP-DIVE]:\n{night_data['lore']}")
        elif action == '4':
            print(f"\n[EASTER EGGS & GLITCHES]:\n{night_data['easter_eggs']}")
        elif action == '5':
            q = input("\nEnter custom question for local AI: ").strip()
            print("\nAnalyzing engine data...")
            print(f"\nDispatcher:\n{query_ollama(q, night_data)}")
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

