import streamlit as st
from dataclasses import dataclass
from typing import Dict
from collections import defaultdict


# -----------------------------
# Représentation des règles
# -----------------------------

@dataclass
class Rule:
    id: str
    conditions: Dict[str, str]
    destination: str
    score: int
    explanation: str


RULES = [

Rule("R1",{"budget":"faible","climat":"chaud"},"Maroc",3,
"Budget faible et climat chaud → Maroc"),

Rule("R2",{"budget":"faible","activites":"plage"},"Espagne",2,
"Budget faible et activité plage → Espagne"),

Rule("R3",{"budget":"faible","ambiance":"calme"},"Portugal",2,
"Budget faible et ambiance calme → Portugal"),

Rule("R4",{"budget":"moyen","climat":"chaud"},"Grèce",3,
"Budget moyen et climat chaud → Grèce"),

Rule("R5",{"budget":"moyen","climat":"tempere","activites":"monuments"},"Italie",3,
"Budget moyen, climat tempéré et monuments → Italie"),

Rule("R6",{"budget":"moyen","ambiance":"familiale"},"Portugal",2,
"Budget moyen et ambiance familiale → Portugal"),

Rule("R7",{"budget":"moyen","activites":"gastronomie"},"Italie",2,
"Budget moyen et gastronomie → Italie"),

Rule("R8",{"budget":"eleve","ambiance":"nature"},"Islande",4,
"Budget élevé et nature → Islande"),

Rule("R9",{"budget":"eleve","distance":"lointaine"},"Thaïlande",4,
"Budget élevé et destination lointaine → Thaïlande"),

Rule("R10",{"budget":"eleve","climat":"froid"},"Norvège",3,
"Budget élevé et climat froid → Norvège"),

Rule("R11",{"saison":"ete","activites":"plage"},"Grèce",2,
"Été et plage → Grèce"),

Rule("R12",{"saison":"hiver","ambiance":"calme"},"Finlande",3,
"Hiver et ambiance calme → Finlande"),

Rule("R13",{"saison":"printemps","activites":"nature"},"Portugal",2,
"Printemps et nature → Portugal"),

Rule("R14",{"ambiance":"fetarde","climat":"chaud"},"Espagne",3,
"Ambiance fêtarde et climat chaud → Espagne"),

Rule("R15",{"activites":"randonnee","climat":"froid"},"Islande",4,
"Randonnée et climat froid → Islande"),

Rule("R16",{"budget":"moyen","distance":"proche"},"France",2,
"Budget moyen et destination proche → France"),

Rule("R17",{"budget":"eleve","activites":"shopping"},"Dubaï",4,
"Budget élevé et shopping → Dubaï"),

Rule("R18",{"climat":"chaud","activites":"plage"},"Bali",3,
"Climat chaud et plage → Bali"),

Rule("R19",{"climat":"tempere","ambiance":"romantique"},"Venise",3,
"Climat tempéré et romantique → Venise"),

Rule("R20",{"activites":"nature","distance":"proche"},"Suisse",3,
"Nature et destination proche → Suisse"),

]


# -----------------------------
# Images destinations
# -----------------------------

DESTINATION_IMAGES = {

"Maroc":"https://source.unsplash.com/600x400/?morocco",
"Espagne":"https://source.unsplash.com/600x400/?spain",
"Portugal":"https://source.unsplash.com/600x400/?portugal",
"Grèce":"https://source.unsplash.com/600x400/?greece",
"Italie":"https://source.unsplash.com/600x400/?italy",
"Islande":"https://source.unsplash.com/600x400/?iceland",
"Thaïlande":"https://source.unsplash.com/600x400/?thailand",
"Norvège":"https://source.unsplash.com/600x400/?norway",
"Finlande":"https://source.unsplash.com/600x400/?finland",
"France":"https://source.unsplash.com/600x400/?paris",
"Dubaï":"https://source.unsplash.com/600x400/?dubai",
"Bali":"https://source.unsplash.com/600x400/?bali",
"Venise":"https://source.unsplash.com/600x400/?venice",
"Suisse":"https://source.unsplash.com/600x400/?switzerland"

}


# -----------------------------
# Vérifier conditions
# -----------------------------

def match(rule,facts):

    for k,v in rule.conditions.items():

        if facts.get(k)!=v:
            return False

    return True


# -----------------------------
# Moteur d'inférence
# -----------------------------

def inference(facts):

    scores = defaultdict(int)
    explanations = defaultdict(list)

    for rule in RULES:

        if match(rule,facts):

            scores[rule.destination]+=rule.score
            explanations[rule.destination].append(rule.explanation)

    return scores,explanations


# -----------------------------
# Interface Streamlit
# -----------------------------

st.title("🌍 Système expert de recommandation de voyage")

st.write("Répondez aux questions pour obtenir des destinations adaptées.")


budget = st.selectbox("Budget",["faible","moyen","eleve"])
climat = st.selectbox("Climat",["chaud","tempere","froid"])
saison = st.selectbox("Saison",["ete","hiver","printemps","automne"])
ambiance = st.selectbox("Ambiance",["calme","aventure","familiale","romantique","fetarde","nature"])
activites = st.selectbox("Activité principale",["plage","randonnee","monuments","shopping","nature","gastronomie"])
distance = st.selectbox("Distance",["proche","moyenne","lointaine"])


facts = {

"budget":budget,
"climat":climat,
"saison":saison,
"ambiance":ambiance,
"activites":activites,
"distance":distance

}


if st.button("Recommander une destination"):

    scores,explanations = inference(facts)

    if not scores:

        st.error("Aucune destination trouvée")

    else:

        sorted_dest = sorted(scores.items(),key=lambda x:x[1],reverse=True)

        st.subheader("🏆 Top destinations")

        for i,(dest,score) in enumerate(sorted_dest[:3],1):

            st.write(f"### {i}. {dest}")

            if dest in DESTINATION_IMAGES:
                st.image(DESTINATION_IMAGES[dest],width=500)

            st.write(f"Score : {score}")

            st.write("Pourquoi :")

            for e in explanations[dest]:
                st.write("•",e)
